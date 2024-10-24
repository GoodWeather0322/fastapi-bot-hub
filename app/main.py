# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager

from app.routers import router
from app.utils.config import settings
from app.services.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動排程器
    scheduler.start()

    yield

    # 關閉排程器
    scheduler.shutdown()


app = FastAPI(title="fastapi-bot", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.router, prefix="/api")
