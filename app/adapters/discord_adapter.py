import discord
from discord import app_commands
from discord.ext import commands
from app.utils.logging_config import logging

logger = logging.getLogger(__name__)


class DiscordAdapter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="weather", description="查詢天氣")
    async def weather(self, interaction: discord.Interaction):
        logger.info(f"slash weather command!")
        await interaction.response.send_message("查詢天氣")


class DiscordAdapterSample(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx: commands.Context):
        logger.info(f"normal hello command!")
        await ctx.send(f"Hello, {ctx.author.mention}!")

    @app_commands.command(name="hello", description="Hello, world!")
    async def slash_hello(self, interaction: discord.Interaction):
        logger.info(f"slash hello command!")
        await interaction.response.send_message("Hello, world!")

    # 關鍵字觸發
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.content == "listen hello":
            logger.info(f"listen hello command!")
            await message.channel.send("Hello, world!")


async def setup(bot: commands.Bot):
    await bot.add_cog(DiscordAdapterSample(bot))
    await bot.add_cog(DiscordAdapter(bot))
