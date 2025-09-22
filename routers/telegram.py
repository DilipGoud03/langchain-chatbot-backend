from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from services.telegram_service import TelegramService

router = APIRouter(
    prefix='/telegram',
    tags=["Tele-Gram"]
)


@router.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")
            print(data)
            if text != '/start':
                TelegramService()._reply_message(chat_id, text)
            else:
                TelegramService()._start_app(chat_id)
    except Exception as e:
        print("HTTPException", str(e))
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse(status_code=200, content={"ok": True})
