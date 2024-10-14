from app.routers.endpoints import line_router, telegram_router

from fastapi import APIRouter

router = APIRouter()

# 註冊各個BOT的路由
router.include_router(line_router.router, prefix="/line")
router.include_router(telegram_router.router, prefix="/telegram")
# 未來可以繼續添加新的BOT路由
