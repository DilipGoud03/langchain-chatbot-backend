from fastapi import APIRouter, HTTPException, Depends, File, Form, UploadFile
from services.document import DocumentService
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Literal, Any
from services.jwt_service import JWTBearer
from models.document import URLUpload
import os
router = APIRouter(
    prefix="/doc",
    tags=["Document"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(JWTBearer())]
)

ALLOWED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain"
}


@router.post('/upload')
def upload_document(
    file: UploadFile = File(...),
    type: Literal['public', 'private'] = Form(default='public'),
):
    
    try:
        
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="This file not allowed")

        doc = DocumentService().CreateDocument(file, type)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return doc


@router.post('/url/upload')
def upload_url_document(
    data: URLUpload
):
    try:
        doc = DocumentService().CreateUrlDocument(data.url, data.type)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return doc


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
        response = DocumentService().ReadDocuments(
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


@router.delete('/{id:int}')
def delete_document(id: int):
    try:
        response = DocumentService().DeleteDocument(id)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=str(e)
        )
    return JSONResponse(
        content=response, status_code=200
    )
