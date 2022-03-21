import os
import asyncio
import discii

from dotenv import load_dotenv
from discii import commands


class TestBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(prefixes=["."])

    async def on_message_create(self, message: discii.Message):
        print(message)


bot = TestBot()


@bot.on("MESSAGE_CREATE")
async def message_create(message: discii.Message):
    print(message)


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
