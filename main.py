import disnake
from disnake.ext import commands
import config
import os
from dotenv import load_dotenv


load_dotenv()


def get_prefix(bot, message):
    config_data = config.load_config()
    return config_data["PREFIX"]


intents = disnake.Intents.all()
intents.message_content = True


bot = commands.Bot(command_prefix=get_prefix, intents=intents)

@bot.event
async def on_ready():
    print(f"Starting..")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(os.getenv("DISCORD_TOKEN"))
