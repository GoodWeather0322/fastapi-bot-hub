from fastapi import APIRouter, Request, Response
from app.adapters.line_adapter import LineBotAdapter
from app.services.business_logic import BusinessLogic
from app.utils.config import settings

router = APIRouter()
adapter = LineBotAdapter()
business_logic = BusinessLogic()


@router.post("/webhook")
async def linebot_webhook(request: Request):
    body = await request.json()
    events = body.get("events", [])
    replies = []

    for event in events:
        unified_input = adapter.to_unified_input(event)
        unified_output = business_logic.process(unified_input)
        reply_message = adapter.from_unified_output(unified_output)
        replies.append({"replyToken": event["replyToken"], "messages": [reply_message]})

    # 調用LINE Messaging API回覆消息
    # 省略實際的API調用代碼
    return Response(status_code=200)
