from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from langchain_chroma import Chroma
import os
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.chains.llm import LLMChain
from services.utility import UtilityService

from db import SQLALCHEMY_DATABASE_URL
load_dotenv()


class Models:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, verbose=True)
        self._utility_service = UtilityService()

    def pinecone_store(self, index_name):
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        if not pc.has_index(index_name):
            pc.create_index(
                name=index_name,
                dimension=1536,   # match embedding model!
                metric="dotproduct",
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )

        return PineconeVectorStore(embedding=self.embeddings, index_name=index_name)

    def chroma_public_store(self):
        return Chroma(
            collection_name="example_collection",
            embedding_function=self.embeddings,
            persist_directory="./db/chroma_langchain_db",
        )

    def chroma_private_store(self):
        return Chroma(
            collection_name="example_private_collection",
            embedding_function=self.embeddings,
            persist_directory="./db/chroma_langchain_db",
        )

    def sql_chain(self):
        db = SQLDatabase.from_uri(SQLALCHEMY_DATABASE_URL)
        execute_query = QuerySQLDataBaseTool(db=db)
        write_query = create_sql_query_chain(self.llm, db)
        answer_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI assistant that decides whether to use SQL results or general knowledge to answer questions."),
            ("human", """
                Question: {question}

                If this is a database-related question:
                    - Use the SQL Query and SQL Result to answer.
                    - SQL Query: {query}
                    - SQL Result: {result}
                    - Don't use id values and created_at values in your answer.
                    - Provide a natural human-readable interpretation.

                If this is NOT a database-related question:
                    - Ignore SQL and answer using your knowledge base only.
            """),
            ("ai", "Final Answer:"),
        ])

        answer = answer_prompt | self.llm
        chain = (RunnablePassthrough.assign(query=write_query | RunnableLambda(
            self._utility_service.clean_sql_query)).assign(result=itemgetter("query") | execute_query) | answer)
        return chain

    def vector_chain(self, is_logged_in: bool = False):
        if is_logged_in:
            print("User Is Logged-In")
            retriever = self.chroma_private_store(
            ).as_retriever(search_kwargs={"k": 2})
        else:
            print("User Is Log-Out")
            retriever = self.chroma_public_store(
            ).as_retriever(search_kwargs={"k": 2})

        rag_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", "You are an AI assistant for a consulting company. "
                    "Only use the provided context from company documents to answer questions."
                ),
                ("human", "Context:\n{context}\n\nQuestion:\n{input}"),
                ("ai", "Answer (be clear, professional, and factual):")
            ]
        )

        combine_docs_chain = create_stuff_documents_chain(self.llm, rag_prompt)
        print("Combine Docs Chain:", retriever)
        return create_retrieval_chain(retriever, combine_docs_chain)

    def generate_answer(self, query: str, is_logged_in: bool = False):

        sql_response = ''
        if is_logged_in:
            print("SQL Response:", sql_response)
            response = self.sql_chain().invoke({"question": query})
            sql_response = response.content

        vector_chain = self.vector_chain(is_logged_in)
        vector_response = vector_chain.invoke({"input": query})
        print("VECTOR Response:", vector_response)
        new_reponse = self.final_answer(
            sql_response, vector_response['answer'])
        return {'answer': new_reponse}

    def final_answer(self, sql_response, vector_response):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI assistant for answer using provided context."),
            ("human", "Context from SQL:\n{sql_response}\n\nContext from RAG:\n{vector_response}\n\nMerge both contexts into a single, human-readable answer without repeating information."),
            ("ai", "Answer (be clear, and it's short):"),
        ])

        chain = LLMChain(llm=self.llm, prompt=prompt)

        final_answer = chain.run({
            "sql_response": sql_response,
            "vector_response": vector_response
        })
        return final_answer

    def _delete_documents(self, file_path):
        public_vector_store = self.chroma_public_store()
        private_vector_store = self.chroma_private_store()
        public_vector_store.delete(where={"source": file_path})
        private_vector_store.delete(where={"source": file_path})
        return True
