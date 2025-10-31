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
from services.llm_service import LLMService

# ------------------------------------------------------------
# Module: langchain_service
# Description:
#   Centralized handler for LLM interactions, embeddings,
#   and retrieval-augmented generation (RAG) pipelines.
#   Integrates vector databases (Chroma, Pinecone) and SQL reasoning.
# ------------------------------------------------------------

load_dotenv()


# ------------------------------------------------------------
# Class: LangchainService
# Description:
#   Provides high-level methods for:
#     - Managing LLMs and embeddings.
#     - Integrating Chroma vector stores.
#     - Executing SQL-aware question answering.
#     - Combining RAG-based and SQL-based responses.
# ------------------------------------------------------------
class LangchainService:
    # ------------------------------------------------------------
    # Method: __init__
    # Description:
    #   Initializes embeddings, language model, and utility service.
    #   Ensures persistence directory for local vector storage.
    # ------------------------------------------------------------
    def __init__(self):
        os.makedirs("vector_db", exist_ok=True)
        provider_name = os.getenv("MODEL_PROVIDER", "openai").lower()
        self.llm_service = LLMService(provider_name)
        self.llm = self.llm_service.chat_model()
        self.embeddings = self.llm_service.embedding_model()
        self._utility_service = UtilityService()

    # ------------------------------------------------------------
    # Method: chroma_public_store
    # Description:
    #   Returns a Chroma vector store for public documents.
    # ------------------------------------------------------------
    def chroma_public_store(self):
        return Chroma(
            collection_name="example_collection",
            embedding_function=self.embeddings,
            persist_directory="./vector_db/chroma_langchain_db",
        )

    # ------------------------------------------------------------
    # Method: chroma_private_store
    # Description:
    #   Returns a Chroma vector store for private (authenticated) documents.
    # ------------------------------------------------------------
    def chroma_private_store(self):
        return Chroma(
            collection_name="example_private_collection",
            embedding_function=self.embeddings,
            persist_directory="./vector_db/chroma_langchain_db",
        )

    # ------------------------------------------------------------
    # Method: sql_chain
    # Description:
    #   Creates a query chain for database question answering.
    #   - Writes natural language queries to SQL.
    #   - Executes SQL safely (only SELECT operations).
    #   - Combines SQL result interpretation with general knowledge.
    # ------------------------------------------------------------
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
                    - Only perform GET operations, never DELETE or UPDATE.
                    - SQL Query: {query}
                    - SQL Result: {result}
                    - Exclude id and created_at fields from your answer.
                    - Provide a human-readable interpretation.

                If not related to the database:
                    - Ignore SQL and answer using general knowledge.
            """),
            ("ai", "Final Answer:")
        ])

        answer = answer_prompt | self.llm
        chain = (
            RunnablePassthrough
            .assign(query=write_query | RunnableLambda(self._utility_service.clean_sql_query))
            .assign(result=itemgetter("query") | execute_query)
            | answer
        )
        return chain

    # ------------------------------------------------------------
    # Method: vector_chain
    # Description:
    #   Creates a Retrieval-Augmented Generation (RAG) pipeline.
    #   - Uses Chroma retrievers (public/private).
    #   - Generates context-aware answers based on stored docs.
    # ------------------------------------------------------------
    def vector_chain(self, is_logged_in: bool = False):
        if is_logged_in:
            print("Employee is Logged-In")
            retriever = self.chroma_private_store(
            ).as_retriever(search_kwargs={"k": 2})
        else:
            print("Employee is Logged-Out")
            retriever = self.chroma_public_store(
            ).as_retriever(search_kwargs={"k": 2})

        rag_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI assistant for a consulting company. Only use the provided context from company documents."),
            ("human", "Context:\n{context}\n\nQuestion:\n{input}"),
            ("ai", "Answer (be clear, professional, and factual):")
        ])

        combine_docs_chain = create_stuff_documents_chain(self.llm, rag_prompt)
        return create_retrieval_chain(retriever, combine_docs_chain)

    # ------------------------------------------------------------
    # Method: generate_answer
    # Description:
    #   Handles hybrid reasoning (SQL + RAG).
    #   - Executes SQL chain if authenticated.
    #   - Executes vector retrieval always.
    #   - Merges both results into a final coherent answer.
    # ------------------------------------------------------------
    def generate_answer(self, query: str, is_logged_in: bool = False):
        sql_response = ''
        if is_logged_in:
            response = self.sql_chain().invoke({"question": query})
            sql_response = response.content

        print("SQL Response:", sql_response)
        vector_chain = self.vector_chain(is_logged_in)
        vector_response = vector_chain.invoke({"input": query})
        print("VECTOR Response:", vector_response)

        merged_response = self.final_answer(
            sql_response, vector_response['answer'])
        return {'answer': merged_response}

    # ------------------------------------------------------------
    # Method: final_answer
    # Description:
    #   Merges responses from SQL and vector-based results
    #   into a unified, concise, and readable output.
    # ------------------------------------------------------------
    def final_answer(self, sql_response, vector_response):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI assistant that merges responses into one answer."),
            ("human", "Context from SQL:\n{sql_response}\n\nContext from RAG:\n{vector_response}\n\nMerge both contexts into a single, human-readable answer without repetition."),
            ("ai", "Answer (clear and concise):"),
        ])

        chain = LLMChain(llm=self.llm, prompt=prompt)
        final_answer = chain.run({
            "sql_response": sql_response,
            "vector_response": vector_response
        })
        return final_answer

    # ------------------------------------------------------------
    # Method: _delete_documents
    # Description:
    #   Removes document embeddings from both Chroma stores.
    # ------------------------------------------------------------
    def _delete_documents(self, file_path):
        public_vector_store = self.chroma_public_store()
        private_vector_store = self.chroma_private_store()
        public_vector_store.delete(where={"source": file_path})
        private_vector_store.delete(where={"source": file_path})
        return True
