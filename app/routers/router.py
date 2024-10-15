from fastapi import APIRouter
from app.utils.config import settings

router = APIRouter()

# 註冊各個BOT的路由
if settings.BOT_TYPE == "line":
    from app.routers.endpoints import line_router

    router.include_router(line_router.router, prefix="/line")
elif settings.BOT_TYPE == "telegram":
    from app.routers.endpoints import telegram_router

    router.include_router(telegram_router.router, prefix="/telegram")
else:
    raise ValueError(f"Unsupported BOT_TYPE: {settings.BOT_TYPE}")
# 未來可以繼續添加新的BOT路由
