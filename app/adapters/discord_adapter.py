import discord
from discord import app_commands
from discord.ext import commands
from app.utils.logging_config import logging
from app.services import services

logger = logging.getLogger(__name__)


class DiscordAdapter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.load_config()

    def load_config(self):
        config = services.config
        for item in config:
            slash_command = self.create_slash_command(item)
            self.bot.tree.add_command(slash_command)

    def create_slash_command(self, item):
        function = getattr(services, item["function"], None)

        async def command_callback(interaction: discord.Interaction):
            result = await function()
            await interaction.response.send_message(result)

        slash_command = app_commands.Command(
            name=item["name"],
            description=item["description"],
            callback=command_callback,
        )

        return slash_command


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
    # await bot.add_cog(DiscordAdapterSample(bot))
    await bot.add_cog(DiscordAdapter(bot))
