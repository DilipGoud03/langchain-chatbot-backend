import os
from uuid import uuid4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.langchain_service import LangchainService
from services.document_reader import DocumentReader
from sql.cruds import documents as document_crud
from utils.logger import logger
import db


# ------------------------------------------------------------
# Module: document_ingestion_service
# Description:
#   Provides a service class for reading, splitting, and storing
#   documents into public/private vector databases for AI search
#   and retrieval. Wraps ingestion logic into a reusable service.
# ------------------------------------------------------------


class DocumentIngestionService:
    # ------------------------------------------------------------
    # Initialize Dependencies
    # ------------------------------------------------------------
    def __init__(self):
        self.langchain_service = LangchainService()
        self.document_reader = DocumentReader()
        self.__db = db.get_db()

        # Define constants
        self.data_folder = "./documents"
        self.chunk_size = 1000
        self.chunk_overlap = 100

        # Initialize vector stores
        self.public_vector_store = self.langchain_service.chroma_public_store()
        self.private_vector_store = self.langchain_service.chroma_private_store()

    # ------------------------------------------------------------
    # Function: ingest_file
    # Description:
    #   Reads and processes a file, splits it into text chunks, and
    #   uploads the resulting documents to the appropriate vector store.
    #   - Supports both 'public' and 'private' storage.
    #   - Automatically handles unique document IDs for vector indexing.
    # ------------------------------------------------------------
    def ingest_file(self, path: str, type: str = 'public') -> bool:
        try:
            logger.info(f"Starting ingestion for file: {path} | Type: {type}")

            # Load and split the document into smaller chunks
            loaded_documents = self.document_reader.file_loader(path)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=len,
                separators=["\n", " ", ""]
            )
            documents = text_splitter.split_documents(loaded_documents)
            uuids = [str(uuid4()) for _ in range(len(documents))]

            logger.info(f"Prepared {len(documents)} document chunks for vector storage.")

            # Add documents to vector stores based on type
            if type == 'private':
                logger.info("Uploading to private vector store...")
                self.private_vector_store.add_documents(documents=documents, ids=uuids)
            else:
                logger.info("Uploading to both public and private vector stores...")
                self.private_vector_store.add_documents(documents=documents, ids=uuids)
                self.public_vector_store.add_documents(documents=documents, ids=uuids)

            logger.info(f"File successfully ingested: {path}")
            return True

        except Exception as e:
            logger.error(f"Error ingesting file '{path}': {str(e)}", exc_info=True)
            return False

    # ------------------------------------------------------------
    # Function: main_loop
    # Description:
    #   Continuously scans the `documents/` folder for unprocessed files.
    #   - Detects document type (public/private) from filename.
    #   - Ingests each new file into vector stores.
    #   - Renames processed files by prefixing with '_'.
    #   - Updates the document path in the database.
    # ------------------------------------------------------------
    def main_loop(self) -> bool:
        logger.info("Background scheduler main_loop started.")
        processed_files = []

        try:
            for filename in os.listdir(self.data_folder):
                if not filename.startswith("_"):
                    file_path = os.path.join(self.data_folder, filename)
                    doc_type = 'private' if filename.startswith('private') else 'public'

                    logger.info(f"Processing new file: {filename} | Type: {doc_type}")
                    success = self.ingest_file(file_path, doc_type)

                    if not success:
                        logger.warning(f"Skipping file due to ingestion failure: {filename}")
                        continue

                    # Mark the document as processed in DB
                    new_filename = "_" + filename
                    document = document_crud._get_document_by_dir_name(self.__db, filename)

                    if document:
                        document.doc_path = str(new_filename)  # type: ignore
                        self.__db.add(document)
                        self.__db.commit()
                        self.__db.refresh(document)
                        logger.debug(f"Updated DB record for file: {filename}")

                    # Rename processed file
                    new_file_path = os.path.join(self.data_folder, new_filename)
                    os.rename(file_path, new_file_path)
                    processed_files.append(file_path)

            logger.info(f"Main loop completed. Total files processed: {len(processed_files)}")
            return True

        except Exception as e:
            logger.error(f"Error in main_loop: {str(e)}", exc_info=True)
            return False
