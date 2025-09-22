import db
import os
from decouple import config
from dotenv import load_dotenv
from sql.cruds import documents as document_crud
import uuid
from services.models import Models
from services.ingest import ingest_file
import validators
from middleware.auth_middleware import get_current_user
load_dotenv()


class DocumentService():
    def __init__(self):
        self.__db = db.get_db()
        self.__dir_name = str(config("DIR_NAME")).strip()
        self.__opne_ai_model = Models()

    def CreateDocument(self, file, type: str):
        try:
            user = get_current_user()
            if not user and user.user_type != 'admin':
                raise PermissionError("Access denied")

            filename = (f'{file.filename}').strip()
            exist_document = document_crud._get_document_by_original_name(
                self.__db, filename)
            if exist_document:
                raise ValueError(
                    "Please rename this file because this is already exist in our record.")

            os.makedirs(self.__dir_name, exist_ok=True)
            extenssion = os.path.splitext(file.filename)[1].lower()
            file_name = f"{type}_{uuid.uuid4().hex}{extenssion}"

            file_path = os.path.join(self.__dir_name, file_name)
            with open(file_path, "wb") as out_file:
                out_file.write(file.file.read())

            doc_data = {
                "original_path": filename,
                "doc_path": file_name,
                "type": type
            }
            doc = document_crud.create_doc(self.__db, doc_data, user.id)
            return doc
        except Exception as e:
            raise ProcessLookupError(str(e))

    def ReadDocuments(
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

            docs = document_crud.list_documents(
                self.__db,
                filter,
                order_by,
                order_direction,
                limit,
                type,
                page,
            )

            all = docs["all_items"]
            documents = docs["docs"]
            meta = {
                "current_item": len(documents),
                "limit": limit,
                "page": page,
                "total_items": all
            }
            return {
                "meta": meta,
                "documents": documents
            }

        except Exception as e:
            raise ProcessLookupError(str(e))

    def DeleteDocument(self, id: int):
        try:
            logged_in_user = get_current_user()
            file = document_crud._get_document_by_id(self.__db, id)
            if not logged_in_user and logged_in_user.user_type != 'admin':
                raise PermissionError('Access denied')
            if file:
                filepath = ''
                _path = str(file.doc_path)
                self.__db.delete(file)
                if validators.url(_path):
                    filepath = _path
                else:
                    file_path = os.path.join(self.__dir_name, _path)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        filepath = file_path.replace('_', '')
                if filepath != '':
                    self.__opne_ai_model._delete_documents(filepath)
                self.__db.commit()
                return "Document has deleted"
            raise ValueError("Document not found for provided id")
        except Exception as e:
            raise ProcessLookupError(str(e))

    def CreateUrlDocument(self, url, type: str):
        try:
            user = get_current_user()
            if not user and user.user_type != 'admin':
                raise PermissionError("Access denied")

            ingest_file(url, type)
            filename = url.split('/')[-1]

            doc_data = {
                "original_path": filename,
                "doc_path": url,
                "type": type
            }
            doc = document_crud.create_doc(self.__db, doc_data, user.id)
            return doc
        except Exception as e:
            print(f"Exception {str(e)}")
            raise ProcessLookupError(str(e))
