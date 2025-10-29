from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from services.telegram_service import TelegramService

# ------------------------------------------------------------
# Router: Telegram
# Description:
#   Handles Telegram bot webhook events.
#   Receives updates from Telegram servers and processes user messages.
# ------------------------------------------------------------
router = APIRouter(
    prefix='/telegram',
    tags=["Tele-Gram"]
)


# ------------------------------------------------------------
# Endpoint: POST /webhook
# Description:
#   Receives webhook events from Telegram.
#   - Extracts chat ID and message text.
#   - If text is '/start', triggers the start handler.
#   - Otherwise, replies to the user's message using TelegramService.
# ------------------------------------------------------------
@router.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")
            print(data)

            # Handle start command separately
            if text != '/start':
                TelegramService()._reply_message(chat_id, text)
            else:
                TelegramService()._start_app(chat_id)
    except Exception as e:
        print("HTTPException", str(e))
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse(status_code=200, content={"ok": True})
