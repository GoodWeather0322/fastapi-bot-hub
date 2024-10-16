from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
)

from app.services import business_logic
from app.utils.config import settings

configuration = Configuration(access_token=settings.LINE_CHANNEL_ACCESS_TOKEN)
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)


class LineAdapter:
    def __init__(self):
        self.load_config()

    def load_config(self):
        self.config = business_logic.config
        self.command_map = {}
        for item in self.config:
            command = item["name"]
            description = item["description"]
            function = getattr(business_logic, item["function"], None)
            self.command_map[command] = {
                "description": description,
                "function": function,
            }

    async def handle_message(self, event):
        user_text = event.message.text

        if user_text in self.command_map:
            command = self.command_map[user_text]
            result = await command["function"]()
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=result)],
                )
            )
        else:
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)],
                )
            )
