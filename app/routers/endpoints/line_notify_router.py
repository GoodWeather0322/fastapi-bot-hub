from fastapi import APIRouter, HTTPException
import requests
import json
from pathlib import Path

from app.utils.logging_config import logging
from app.utils.config import settings
from app.services.line_notify.enroll_notify import send_line_notify

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/get-token")
async def get_token(code: str, state: str):
    async def check_token(access_token):
        url = "https://notify-api.line.me/api/status"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        data = response.json()
        user = data["target"]
        return user

    async def save_token(user, access_token):
        token_storage_file = Path("./app/services/line_notify/token.json")
        if not token_storage_file.exists():
            with open(token_storage_file, "w") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        with open(token_storage_file, "r") as f:
            user2token = json.load(f)
        if user in user2token:
            raise HTTPException(status_code=400, detail="User already exists")
        user2token[user] = access_token
        with open(token_storage_file, "w") as f:
            json.dump(user2token, f, ensure_ascii=False, indent=4)

    url = "https://notify-bot.line.me/oauth/token"
    if state != settings.LINE_NOTIFY_STATE:
        raise HTTPException(status_code=400, detail="Invalid state")

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://botapi.uaicraft.com/api/line-notify/get-token",
        "client_id": settings.LINE_NOTIFY_CLIENT_ID,
        "client_secret": settings.LINE_NOTIFY_CLIENT_SECRET,
    }
    r = requests.post(url, params=payload)
    data = r.json()
    access_token = data["access_token"]
    user = await check_token(access_token)
    if user == "null." or "null" in user:
        raise HTTPException(status_code=400, detail="Invalid user")
    else:
        await save_token(user, access_token)
        await send_line_notify(
            "goodweather notify 註冊成功，將會收到演唱會釋票通知", access_token
        )
        return "success authorized"
