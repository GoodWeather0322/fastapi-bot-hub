from app.models.common_models import UnifiedInput, UnifiedOutput


class LineBotAdapter:
    def to_unified_input(self, line_event):
        """
        將LINE的輸入事件轉換為統一的輸入格式。
        """
        unified_input = UnifiedInput(
            user_id=line_event["source"]["userId"], text=line_event["message"]["text"]
        )
        return unified_input

    def from_unified_output(self, unified_output):
        """
        將統一的輸出格式轉換為LINE需要的回覆格式。
        """
        line_response = {"type": "text", "text": unified_output.response_text}
        return line_response
