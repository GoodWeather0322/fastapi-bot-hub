config = [
    {
        "name": "weather",
        "description": "查詢天氣",
        "function": "get_weather",
    },
    {
        "name": "buy",
        "description": "買入",
        "function": "get_buy",
    },
]


def get_weather():
    """
    查詢城市天氣
    """
    return "天氣是晴朗的"


def get_buy():
    """
    買入
    """
    return "買入"
