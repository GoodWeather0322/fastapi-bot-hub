from fastapi import APIRouter, Request, Response, HTTPException
import asyncio

import discord
from discord.ext import commands

from app.utils.logging_config import logging
from app.utils.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@router.post("/")
async def hello_world():
    return {"Hello": "World"}


@bot.event
async def on_ready():
    logger.info(f"Bot is ready. 目前登入身份 --> {bot.user}")


# 卸載指令檔案
@bot.command()
async def unload(ctx):
    await bot.unload_extension(f"app.adapters.discord_adapter")
    await ctx.send(f"UnLoaded extension done.")


# 重新載入程式檔案
@bot.command()
async def reload(ctx):
    await bot.reload_extension(f"app.adapters.discord_adapter")
    await ctx.send(f"ReLoaded extension done.")


# 一開始bot開機需載入全部程式檔案
async def load_extensions():
    await bot.load_extension(f"app.adapters.discord_adapter")


# 歡迎訊息
@bot.command()
async def welcome(ctx: commands.Context, member: discord.Member):
    await ctx.send(f"Welcome to {ctx.guild.name},  {member.mention}!")


async def run():
    try:
        await load_extensions()
        await bot.start(settings.DISCORD_TOKEN)
    except KeyboardInterrupt:
        await bot.close()


asyncio.create_task(run())
