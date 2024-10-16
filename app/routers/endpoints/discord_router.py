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
    slash = await bot.tree.sync()
    logger.info(f"Bot is ready. 目前登入身份 --> {bot.user}")
    logger.info(f"載入 {len(slash)} 個斜線指令")


# 卸載指令檔案
@bot.tree.command()
async def unload(interaction: discord.Interaction):
    await bot.unload_extension(f"app.adapters.discord_adapter")
    await interaction.response.send_message(f"UnLoaded extension done.")


# 重新載入程式檔案
@bot.tree.command()
async def reload(interaction: discord.Interaction):
    await bot.reload_extension(f"app.adapters.discord_adapter")
    await interaction.response.send_message(f"ReLoaded extension done.")


# 載入全部指令檔案
async def load_extensions():
    await bot.load_extension(f"app.adapters.discord_adapter")


# 歡迎訊息
@bot.tree.command()
async def welcome(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(
        f"Welcome to {interaction.guild.name},  {member.mention}!"
    )


async def run():
    try:
        await load_extensions()
        await bot.start(settings.DISCORD_TOKEN)
    except KeyboardInterrupt:
        await bot.close()


asyncio.create_task(run())
