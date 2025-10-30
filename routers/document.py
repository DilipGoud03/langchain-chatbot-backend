from fastapi import APIRouter, HTTPException, Depends, File, Form, UploadFile
from services.document import DocumentService
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Literal, Any
from services.jwt_service import JWTBearer
from models.document import URLUpload
import os

# ------------------------------------------------------------
# Router: Document
# Description:
#   Handles document management operations including:
#   - Uploading files or URLs
#   - Listing stored documents
#   - Deleting documents
#   Protected by JWT authentication middleware.
# ------------------------------------------------------------
router = APIRouter(
    prefix="/doc",
    tags=["Document"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(JWTBearer())]  # Requires valid JWT for all routes
)

# ------------------------------------------------------------
# Allowed MIME types for uploaded documents
# ------------------------------------------------------------
ALLOWED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain"
}


# ------------------------------------------------------------
# Endpoint: POST /upload
# Description:
#   Uploads a new document file.
#   Validates MIME type and delegates to DocumentService for saving.
# ------------------------------------------------------------
@router.post('/upload')
def upload_document(
    file: UploadFile = File(...),
    type: Literal['public', 'private'] = Form(default='public'),
):
    try:
        # Validate file type before processing
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="This file type is not allowed")

        # Save document through the service layer
        doc = DocumentService().create_document(file, type)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return doc


# ------------------------------------------------------------
# Endpoint: POST /url/upload
# Description:
#   Uploads a document by providing a remote URL.
# ------------------------------------------------------------
@router.post('/url/upload')
def upload_url_document(data: URLUpload):
    try:
        # Process URL-based document upload
        doc = DocumentService().create_url_document(data.url, data.type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return doc


# ------------------------------------------------------------
# Endpoint: GET /list
# Description:
#   Retrieves a paginated list of documents.
#   Supports filtering, sorting, and pagination.
# ------------------------------------------------------------
@router.get('/list')
def read_documents(
    filter: str = '',
    order_by: str = 'id',
    order_direction: Literal['desc', 'asc'] = 'desc',
    limit: int = 10,
    type: Literal['all', 'public', 'private'] = 'all',
    page: int = 1
):
    try:
        response = DocumentService().read_documents(
            filter,
            order_by,
            order_direction,
            limit,
            type,
            page
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return response


# ------------------------------------------------------------
# Endpoint: DELETE /{id}
# Description:
#   Deletes a specific document by its ID.
# ------------------------------------------------------------
@router.delete('/{id:int}')
def delete_document(id: int):
    try:
        response = DocumentService().delete_document(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Return confirmation of deletion
    return JSONResponse(content=response, status_code=200)
