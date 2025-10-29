from pydantic import BaseModel
from typing import Optional, List

# ------------------------------------------------------------
# Model: Document
# Description:
#   Represents a single stored document record with metadata.
#   Used to track uploaded or processed documents.
# ------------------------------------------------------------
class Document(BaseModel):
    id: Optional[int] = None               # Unique document ID (optional, usually DB-generated)
    original_path: str                     # File path of the original uploaded document
    doc_path: str                          # File path of the processed/stored document
    type: str                              # Document type (e.g., 'pdf', 'video', 'text')
    created_at: Optional[str]              # Timestamp of document creation


# ------------------------------------------------------------
# Model: Meta
# Description:
#   Metadata structure for paginated document responses.
# ------------------------------------------------------------
class Meta(BaseModel):
    current_item: Optional[int]            # Index of the current item in pagination
    total_items: Optional[int]             # Total number of available items
    limit: Optional[int]                   # Max number of items per page
    page: Optional[int]                    # Current page number


# ------------------------------------------------------------
# Model: DocumentList
# Description:
#   Combines pagination metadata and a list of documents.
# ------------------------------------------------------------
class DocumentList(BaseModel):
    meta: Meta                             # Pagination details
    documents: List[Document]              # List of document entries


# ------------------------------------------------------------
# Model: URLUpload
# Description:
#   Schema for uploading a document via a remote URL.
# ------------------------------------------------------------
class URLUpload(BaseModel):
    url: str                               # Remote file URL
    type: str                              # File type (e.g., 'pdf', 'video', 'text')
