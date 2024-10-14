from fastapi import APIRouter, Request
from app.adapters.telegram_adapter import TelegramBotAdapter
from app.services.business_logic import BusinessLogic

router = APIRouter()
adapter = TelegramBotAdapter()
business_logic = BusinessLogic()


@router.post("/webhook")
async def telegrambot_webhook(request: Request):
    body = await request.json()
    unified_input = adapter.to_unified_input(body)
    unified_output = business_logic.process(unified_input)
    reply_message = adapter.from_unified_output(unified_output)

    # 調用Telegram Bot API回覆消息
    # 省略實際的API調用代碼
    return {"ok": True}
