from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from services.models import Models
from models.chat_bot import ChatModel
from middleware.auth_middleware import get_current_user

router = APIRouter(
    prefix='/chat-bot',
    tags=["Chat Bot"],
)

ai_model = Models()

@router.post("/")
def start_chat(
    question: ChatModel
):
    try:
        user = get_current_user()
        is_logged_in = False
        if user:
            is_logged_in = True
        response = ai_model.generate_answer(question.query, is_logged_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return JSONResponse(f"{response['answer']}", status_code=200)
