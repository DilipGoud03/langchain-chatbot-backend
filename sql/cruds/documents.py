from sqlalchemy.orm import Session
from sql.models.documents import Document
from sql.models.employees import Employee
from sqlalchemy import and_, asc, desc, func, or_


# ------------------------------------------------------------
# Module: document_crud
# Description:
#   Provides CRUD operations for the `Document` model.
#   Includes helper methods for filtering, sorting, and pagination.
# ------------------------------------------------------------


# ------------------------------------------------------------
# Method: create_doc
# Description:
#   Creates and stores a new document record in the database.
#
# Parameters:
#   - db (Session): SQLAlchemy database session.
#   - data (dict): Dictionary containing document fields.
#   - employee_id (int): ID of the employee who uploaded the document.
#
# Returns:
#   - Document: The newly created document record.
# ------------------------------------------------------------
def create_doc(db: Session, data: dict, employee_id: int):
    document = Document()
    document.original_path = data.get("original_path", "")
    document.doc_path = data.get("doc_path", "")
    document.type = data.get("type", "")
    document.employee_id = employee_id  # type: ignore

    db.add(document)
    db.commit()
    db.refresh(document)
    return document


# ------------------------------------------------------------
# Method: _get_document_by_original_name
# Description:
#   Retrieves a document using its original filename.
# ------------------------------------------------------------
def _get_document_by_original_name(db: Session, name: str):
    return db.query(Document).filter(Document.original_path == name).first()


# ------------------------------------------------------------
# Method: _get_document_by_dir_name
# Description:
#   Retrieves a document using its stored directory name.
# ------------------------------------------------------------
def _get_document_by_dir_name(db: Session, name: str):
    return db.query(Document).filter(Document.doc_path == name).first()


# ------------------------------------------------------------
# Method: _get_document_by_id
# Description:
#   Retrieves a document by its unique ID.
# ------------------------------------------------------------
def _get_document_by_id(db: Session, id: int) -> Document:
    return db.query(Document).filter(Document.id == id).first()


# ------------------------------------------------------------
# Method: list_documents
# Description:
#   Lists all documents with support for:
#     - Text-based filtering
#     - Employee-specific filtering
#     - Sorting (asc/desc)
#     - Pagination
#     - Document type selection
#
# Parameters:
#   - db (Session): Active SQLAlchemy session.
#   - filter (str): Optional keyword for fuzzy search.
#   - order_by (str): Column name to order by (default: 'id').
#   - order_direction (str): 'asc' or 'desc' (default: 'desc').
#   - limit (int): Number of records per page.
#   - type (str): Filter by document type.
#   - page (int): Current page number.
#   - employee_id (int): Filter by employee (if > 0).
#
# Returns:
#   - dict: Contains total count and list of matching documents.
# ------------------------------------------------------------
def list_documents(
    db: Session,
    filter: str = "",
    order_by: str = "id",
    order_direction: str = "desc",
    limit: int = 10,
    type: str = "",
    page: int = 1,
    employee_id: int = 0
):
    query = db.query(Document).join(
        Employee, Employee.id == Document.employee_id, isouter=True
    )

    # Apply text-based filters
    if filter and filter.strip():
        filter_data = f"%{filter.strip()}%"
        query = query.filter(
            or_(
                Document.id.like(filter_data),
                Document.original_path.like(filter_data),
                Document.doc_path.like(filter_data),
                Document.employee_id.like(filter_data),
                Employee.id.like(filter_data),
                Employee.name.like(filter_data),
                Employee.email.like(filter_data),
            )
        )

    # Filter by employee ID
    if employee_id > 0:
        query = query.filter(Document.employee_id == employee_id)

    # Filter by document type
    if type and type.lower() != "all":
        query = query.filter(Document.type == type)

    # Sort results
    if order_by:
        direction = desc if order_direction == "desc" else asc
        query = query.order_by(direction(getattr(Document, order_by)))

    # Count total items before pagination
    total_items = query.count()

    # Apply pagination
    if limit > 0:
        offset = (int(page) - 1) * limit
        query = query.limit(limit).offset(offset)

    docs = query.all()
    return {
        "all_items": total_items,
        "docs": docs
    }
