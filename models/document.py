from pydantic import BaseModel
from typing import Optional, List


class Document(BaseModel):
    id: Optional[int] = None
    original_path: str
    doc_path: str
    type: str
    created_at: Optional[str]


class Meta(BaseModel):
    current_item: Optional[int]
    total_items: Optional[int]
    limit: Optional[int]
    page: Optional[int]


class DocumentList(BaseModel):
    meta: Meta
    documents: List[Document]


class URLUpload(BaseModel):
    url: str
    type: str
