from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TYPE: str
    LINE_CHANNEL_SECRET: str
    LINE_CHANNEL_ACCESS_TOKEN: str
    LINE_NOTIFY_STATE: str
    LINE_NOTIFY_CLIENT_ID: str
    LINE_NOTIFY_CLIENT_SECRET: str
    TELEGRAM_BOT_TOKEN: str
    DISCORD_TOKEN: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
