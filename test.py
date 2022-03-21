import os
import asyncio

from dotenv import load_dotenv
from discii import commands

bot = commands.Bot(prefixes=["."])

# @bot.on("MESSAGE_CREATE")
# async def message_create(message: discii.Message):
#     print(message)


@bot.command(names=["ping"])
async def ping(context: commands.Context):
    await context.send(f"The bots ping is **{round(bot.latency*1000)}**")


@bot.command(names=["add"])
async def add(context: commands.Context, num1: int, num2: int):
    await context.send(f"{num1 + num2 = }")


# @bot.error(command=True)
# async def command_error(context: commands.Context, error):
#     print(context, error)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(bot.start(os.environ["BOT_TOKEN"]))
