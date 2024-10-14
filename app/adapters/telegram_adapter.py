from app.models.common_models import UnifiedInput, UnifiedOutput


class TelegramBotAdapter:
    def to_unified_input(self, telegram_update):
        """
        將Telegram的更新消息轉換為統一的輸入格式。
        """
        unified_input = UnifiedInput(
            user_id=str(telegram_update["message"]["from"]["id"]),
            text=telegram_update["message"]["text"],
        )
        return unified_input

    def from_unified_output(self, unified_output):
        """
        將統一的輸出格式轉換為Telegram需要的回覆格式。
        """
        telegram_response = {"text": unified_output.response_text}
        return telegram_response
