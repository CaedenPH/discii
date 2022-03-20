import os
import asyncio

from dotenv import load_dotenv
from discii import commands

bot = commands.Bot(prefixes=["."])


@bot.command(names=["ping"])
async def ping(context: commands.Context):
    await context.send(f"{round(bot.latency*1000)}")


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(bot.start(os.environ["BOT_TOKEN"]))
