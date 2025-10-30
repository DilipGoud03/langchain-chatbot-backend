import db
import os
from decouple import config
from dotenv import load_dotenv
from sql.cruds import documents as document_crud
import uuid
from services.langchain_service import LangchainService
from services.document_ingestion_service import DocumentIngestionService
import validators
from middleware.auth_middleware import get_current_employee


# ------------------------------------------------------------
# Service: DocumentService
# Description:
#   Handles creation, retrieval, deletion, and ingestion of
#   documents (file or URL-based). Integrates with LangChain
#   and OpenAI models for indexing, vectorization, and search.
# ------------------------------------------------------------

load_dotenv()


class DocumentService:
    # ------------------------------------------------------------
    # Constructor
    # Description:
    #   Initializes the database connection, document directory,
    #   OpenAI/LangChain service instance, and ingestion service.
    # ------------------------------------------------------------
    def __init__(self):
        self.__db = db.get_db()
        self.__dir_name = str(config("DIR_NAME")).strip()
        self.__opne_ai_model = LangchainService()
        self.__ingestion_service = DocumentIngestionService()

    # ------------------------------------------------------------
    # Method: create_document
    # Description:
    #   Handles local file upload and database record creation.
    #   - Validates user access (admin only).
    #   - Prevents duplicate file names.
    #   - Saves file to disk and stores metadata in the database.
    # ------------------------------------------------------------
    def create_document(self, file, type: str):
        try:
            employee = get_current_employee()
            if not employee and employee.employee_type != 'admin':
                raise PermissionError("Access denied")

            # Check for duplicate document names
            filename = (f'{file.filename}').strip()
            exist_document = document_crud._get_document_by_original_name(self.__db, filename)
            if exist_document:
                raise ValueError(
                    "Please rename this file because it already exists in our records."
                )

            # Ensure directory exists
            os.makedirs(self.__dir_name, exist_ok=True)

            # Generate unique file name
            extension = os.path.splitext(file.filename)[1].lower()
            file_name = f"{type}_{uuid.uuid4().hex}{extension}"
            file_path = os.path.join(self.__dir_name, file_name)

            # Save file to disk
            with open(file_path, "wb") as out_file:
                out_file.write(file.file.read())

            # Create DB record
            doc_data = {
                "original_path": filename,
                "doc_path": file_name,
                "type": type
            }

            doc = document_crud.create_doc(self.__db, doc_data, employee.id)
            return doc

        except Exception as e:
            raise ProcessLookupError(str(e))

    # ------------------------------------------------------------
    # Method: read_documents
    # Description:
    #   Retrieves paginated list of documents with metadata.
    #   - Supports filters, sorting, pagination, and type filters.
    # ------------------------------------------------------------
    def read_documents(
        self,
        filter: str = '',
        order_by: str = 'id',
        order_direction: str = 'desc',
        limit: int = 10,
        type: str = 'all',
        page: int = 1
    ):
        try:
            if limit < 1:
                limit = 10
            if page < 1:
                page = 1

            # Fetch paginated document data
            docs = document_crud.list_documents(
                self.__db,
                filter,
                order_by,
                order_direction,
                limit,
                type,
                page,
            )

            all_items = docs["all_items"]
            documents = docs["docs"]

            meta = {
                "current_item": len(documents),
                "limit": limit,
                "page": page,
                "total_items": all_items
            }

            return {
                "meta": meta,
                "documents": documents
            }

        except Exception as e:
            raise ProcessLookupError(str(e))

    # ------------------------------------------------------------
    # Method: delete_document
    # Description:
    #   Deletes a document by ID from both database and file system.
    #   - Validates admin access.
    #   - Removes physical file (if applicable).
    #   - Deletes associated vectors from the vector database.
    # ------------------------------------------------------------
    def delete_document(self, id: int):
        try:
            logged_in_employee = get_current_employee()
            file = document_crud._get_document_by_id(self.__db, id)

            if not logged_in_employee and logged_in_employee.employee_type != 'admin':
                raise PermissionError('Access denied')

            if file:
                filepath = ''
                _path = str(file.doc_path)

                # Delete database record
                self.__db.delete(file)

                # Determine file source (local or remote)
                if validators.url(_path):
                    filepath = _path
                else:
                    file_path = os.path.join(self.__dir_name, _path)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        filepath = file_path.replace('_', '')

                # Delete vectors from LangChain store
                if filepath != '':
                    self.__opne_ai_model._delete_documents(filepath)

                self.__db.commit()
                return "Document has been deleted successfully."

            raise ValueError("Document not found for the provided ID.")

        except Exception as e:
            raise ProcessLookupError(str(e))

    # ------------------------------------------------------------
    # Method: create_url_document
    # Description:
    #   Creates a new document entry from a remote file or webpage URL.
    #   - Validates admin access.
    #   - Uses DocumentIngestionService to process and index the file.
    #   - Stores metadata in the database for retrieval.
    # ------------------------------------------------------------
    def create_url_document(self, url, type: str):
        try:
            employee = get_current_employee()
            if not employee and employee.employee_type != 'admin':
                raise PermissionError("Access denied")

            # Ingest document from URL into vector stores
            self.__ingestion_service.ingest_file(url, type)
            filename = url.split('/')[-1]

            # Create DB record
            doc_data = {
                "original_path": filename,
                "doc_path": url,
                "type": type
            }

            doc = document_crud.create_doc(self.__db, doc_data, employee.id)
            return doc

        except Exception as e:
            print(f"Exception {str(e)}")
            raise ProcessLookupError(str(e))
