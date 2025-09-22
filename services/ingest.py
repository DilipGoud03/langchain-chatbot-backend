import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4
from services.models import Models
from sql.cruds import documents as document_crud
import db
from services.file_reader import FileReader
# Initialize the model
model = Models()
file_reader = FileReader()
__db = db.get_db()
# Define constants
data_folder = "./documents"
chunk_size = 1000
chunk_overlap = 100
public_vector_store = model.chroma_public_store()
private_vector_store = model.chroma_private_store()


def ingest_file(path, type: str = 'public'):
    print(f"Starting to ingest file: {path}")
    print(f"Your Document is {type}")

    loaded_documents = file_reader.file_loader(path)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len, separators=[
            "\n", " ", ""]
    )
    documents = text_splitter.split_documents(loaded_documents)
    uuids = [str(uuid4()) for _ in range(len(documents))]
    print(f"Adding {len(documents)} documents to the vector store")
    if type == 'private':
        print("=================Call the private store=================")
        private_vector_store.add_documents(documents=documents, ids=uuids)
    else:
        print("=================Call both stores=================")
        private_vector_store.add_documents(documents=documents, ids=uuids)
        public_vector_store.add_documents(documents=documents, ids=uuids)
    print(f"Finishing ingesting file: {path}")
    return True


def main_loop():
    print('Background scheduler has start and it is in main_loop')
    process_path = []
    for filename in os.listdir(data_folder):
        if not filename.startswith("_"):
            file_path = os.path.join(data_folder, filename)
            doc_type = 'public'
            if filename.startswith('private'):
                doc_type = 'private'
            ingest_file(file_path, doc_type)
            new_filename = "_" + filename
            document = document_crud._get_document_by_dir_name(__db, filename)
            if document:
                document.doc_path = str(new_filename)  # type: ignore
                __db.add(document)
                __db.commit()
                __db.refresh(document)
            new_file_path = os.path.join(data_folder, new_filename)
            process_path.append(file_path)
            os.rename(file_path, new_file_path)
    print('Number of file are proccessed', process_path)
    return True
