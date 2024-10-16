from fastapi import APIRouter, Request, Response, HTTPException

from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError

from app.adapters.line_adapter import LineAdapter
from app.utils.logging_config import logging
from app.utils.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()
adapter = LineAdapter()

parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@router.post("/webhook")
async def linebot_webhook(request: Request):
    # get X-Line-Signature header value
    signature = request.headers.get("x-line-signature")

    body = await request.body()
    body = body.decode("utf-8")

    logger.info("Request body: " + body)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(
            event.message, TextMessageContent
        ):
            await adapter.handle_message(event)
        else:
            logger.info(f"Unsupported event type: {type(event)}")
    return "OK"
