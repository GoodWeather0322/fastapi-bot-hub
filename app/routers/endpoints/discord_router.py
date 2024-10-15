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
    logger.info(f"Bot is ready. Logged in as {bot.user}")


@bot.command()
async def welcome(ctx: commands.Context, member: discord.Member):
    await ctx.send(f"Welcome to {ctx.guild.name},  {member.mention}!")


async def run():
    try:
        await bot.start(settings.DISCORD_TOKEN)
    except KeyboardInterrupt:
        await bot.close()


asyncio.create_task(run())
