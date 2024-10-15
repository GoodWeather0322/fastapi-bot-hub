from fastapi import APIRouter, Request, Response, HTTPException

from linebot import WebhookHandler
from linebot.v3.messaging import Configuration
from linebot.v3.exceptions import InvalidSignatureError

from app.adapters.line_adapter import LineBotAdapter
from app.services.business_logic import BusinessLogic
from app.utils.config import settings
from app.utils.logging_config import logging

logger = logging.getLogger(__name__)

router = APIRouter()
adapter = LineBotAdapter()
business_logic = BusinessLogic()

configuration = Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


@router.post("/webhook")
async def linebot_webhook(request: Request):
    # get X-Line-Signature header value
    signature = request.headers.get("x-line-signature")

    body = await request.body()
    body = body.decode("utf-8")

    logger.info("Request body: " + body)

    # TODO: 把handler放到Adapter嗎?，Adapter有沒有必要性，怎麼設計多個BOT

    # handle webhook body
    # try:
    #     handler.handle(body, signature)
    # except InvalidSignatureError:
    #     logger.error(
    #         "Invalid signature. Please check your channel access token/channel secret."
    #     )
    #     raise HTTPException(status_code=400, detail="Invalid signature")

    return "OK"
    # body = await request.json()
    # events = body.get("events", [])
    # replies = []

    # for event in events:
    #     unified_input = adapter.to_unified_input(event)
    #     unified_output = business_logic.process(unified_input)
    #     reply_message = adapter.from_unified_output(unified_output)
    #     replies.append({"replyToken": event["replyToken"], "messages": [reply_message]})

    # # 調用LINE Messaging API回覆消息
    # # 省略實際的API調用代碼
    # return Response(status_code=200)


# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event):
#     with ApiClient(configuration) as api_client:
#         line_bot_api = MessagingApi(api_client)
#         line_bot_api.reply_message_with_http_info(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=event.message.text)],
#             )
#         )
