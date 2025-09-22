from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from services.whatsapp_service import WhatsAppService
from fastapi.requests import Request
from decouple import config
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix='/whatsapp',
    tags=["What'sApp"]
)


@router.get("/webhook")
async def verify_whatsapp_webhook(
    hub_mode=Query(alias='hub.mode'),
    hub_challenge=Query(alias='hub.challenge'),
    hub_verify_token=Query(alias='hub.verify_token')
):
    if hub_mode == "subscribe" and hub_verify_token == config('VERIFY_TOKEN'):
        return PlainTextResponse(content=hub_challenge, status_code=200)
    else:
        return PlainTextResponse(content="Forbidden", status_code=403)


@router.post("/webhook")
async def reply_incoming_message(request: Request):
    body = await request.body()
    if not body:
        raise HTTPException(status_code=400, detail="request body not found")
    try:
        data = await request.json()
        if "entry" in data:
            for entry in data["entry"]:
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    print(data)
                    for msg in messages:
                        from_number = msg["from"]
                        text = msg.get("text", {}).get("body")
                        if text:
                            WhatsAppService().reply_whatsapp_message(from_number, text)
        return JSONResponse("message: Ok", status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
