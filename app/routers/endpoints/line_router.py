from fastapi import APIRouter, Request, Response, HTTPException

from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.exceptions import InvalidSignatureError

from app.adapters.line_adapter import LineBotAdapter
from app.utils.logging_config import logging
from app.utils.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()
adapter = LineBotAdapter()

configuration = Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@router.post("/webhook")
async def linebot_webhook(request: Request):
    # get X-Line-Signature header value
    signature = request.headers.get("x-line-signature")

    body = await request.body()
    body = body.decode("utf-8")

    # logger.info("Request body: " + body)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue
        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)],
            )
        )

    return "OK"
