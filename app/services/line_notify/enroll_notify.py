from pathlib import Path
import json
import requests
from bs4 import BeautifulSoup

from app.services.scheduler import scheduler
from app.utils.logging_config import logging

logger = logging.getLogger(__name__)


async def send_line_notify(message, access_token):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"message": message}
    response = requests.post(url, headers=headers, params=payload)
    return response


async def send_line_notify_to_all(message):
    token_storage_file = Path("./app/services/line_notify/token.json")
    with open(token_storage_file, "r") as f:
        user2token = json.load(f)
    for user, access_token in user2token.items():
        response = await send_line_notify(message, access_token)
        if response.status_code != 200:
            print(f"Failed to send message to {user}")


async def crawl_ticket_info():
    result_text = []
    # 目標 URL
    url = "https://tixcraft.com/activity/game/24_jaychou"
    # url = "https://tixcraft.com/activity/game/25_keshi_v"

    # 發送 GET 請求
    response = requests.get(url)

    # 確認請求成功
    if response.status_code == 200:
        # 解析 HTML 內容
        soup = BeautifulSoup(response.text, "html.parser")

        # 這裡可以根據網頁結構提取所需的信息
        # 例如，提取所有的標題
        table = soup.find("table", {"class": "table table-bordered"})
        trs = table.find_all("tr")
        for tr in trs:
            button = tr.find("button")
            if button:
                message = f"{tr.get_text()} => 發現釋票"
                result_text.append(message)
    else:
        logger.error(
            f"Failed to retrieve the page. Status code: {response.status_code}"
        )

    # ============
    if result_text:
        result_message = "\n".join(result_text)
        result_message = (
            "\nhttps://tixcraft.com/activity/game/24_jaychou\n" + result_message
        )
        await send_line_notify_to_all(result_message)


scheduler.add_job(crawl_ticket_info, "interval", seconds=10)
