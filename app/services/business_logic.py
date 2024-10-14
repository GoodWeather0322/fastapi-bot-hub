class BusinessLogic:
    def process(self, unified_input):
        """
        處理統一格式的輸入數據，返回統一格式的輸出數據。
        """
        # 這裡是你的業務邏輯，實現具體的處理流程
        # 假設業務邏輯是將輸入文本轉換為大寫
        output = {"response_text": unified_input["text"].upper()}
        return output
