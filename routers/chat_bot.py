from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from services.langchain_service import LangchainService
from models.chat_bot import ChatModel
from middleware.auth_middleware import get_current_employee

# ------------------------------------------------------------
# Router: Chat Bot
# Description:
#   Handles chat requests between users and the AI model.
#   Provides a single endpoint for generating AI-based responses.
# ------------------------------------------------------------
router = APIRouter(
    prefix='/chat-bot',
    tags=["Chat Bot"],
)

# Initialize the AI model service
langchain_service = LangchainService()


# ------------------------------------------------------------
# Endpoint: POST /
# Description:
#   Starts a new chat session or processes a user question.
#   - Accepts a query input from the user.
#   - Checks if the user is logged in.
#   - Returns the AI-generated answer.
# ------------------------------------------------------------
@router.post("/")
def start_chat(question: ChatModel):
    try:
        employee = get_current_employee()      # Retrieve currently authenticated user
        is_logged_in = bool(employee)          # Flag login status for context-aware response
        response = langchain_service.generate_answer(question.query, is_logged_in)  # Get AI response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Return the AI's answer as a JSON response
    return JSONResponse(f"{response['answer']}", status_code=200)
