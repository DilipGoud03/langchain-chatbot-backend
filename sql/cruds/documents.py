from sqlalchemy.orm import Session
from sql.models.documents import Document
from sql.models.users import User
from sqlalchemy import and_, asc, desc, func, or_


def create_doc(db: Session, data: dict, user_id: int):
    document = Document()
    document.original_path = data.get("original_path", '')
    document.doc_path = data.get("doc_path", '')
    document.type = data.get("type", '')
    document.user_id = user_id # type: ignore
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def _get_document_by_original_name(db: Session, name: str):
    return db.query(Document).filter(Document.original_path == name).first()


def _get_document_by_dir_name(db: Session, name: str):
    return db.query(Document).filter(Document.doc_path == name).first()


def _get_document_by_id(db: Session, id: int) -> Document:
    return db.query(Document).filter(Document.id == id).first()


def list_documents(
    db: Session,
    filter: str = '',
    order_by: str = 'id',
    order_direction: str = 'desc',
    limit: int = 10,
    type: str = '',
    page: int = 1,
    user_id: int = 0
):

    query = db.query(Document).join(
        User, User.id == Document.user_id, isouter=True)

    if filter and filter != "":
        filter_data = "%{}%".format(filter.strip())
        query = query.filter(
            or_(
                Document.id.like(filter_data),
                Document.original_path.like(filter_data),
                Document.doc_path.like(filter_data),
                Document.user_id.like(filter_data),
                User.id.like(filter_data),
                User.name.like(filter_data),
                User.email.like(filter_data),
            )

        )

    if user_id and user_id > 0:
        query = query.filter(Document.user_id == user_id)

    if type and type != 'all':
        query = query.filter(Document.type == type)

    if order_by and order_by != "":
        dicrection = desc if order_direction == 'desc' else asc
        query = query.order_by(dicrection(getattr(Document, order_by)))

    all = query.count()

    if limit and limit > 0:
        query = query.limit(limit)
        offset = (int(page) - 1) * limit
        query = query.offset(offset)

    docs = query.all()
    return {
        "all_items": all,
        "docs": docs
    }
