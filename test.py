import os
import asyncio
import discii

from dotenv import load_dotenv

client = discii.Client()


@client.on("READY")
async def bot_ready() -> None:
    print(f"The client is ready. The client's latency is {round(client.latency * 1000)}s")


@client.on("MESSAGE_CREATE")
async def on_message(message: discii.Message):
    print(f"Message detected. Message content: {message.content}")

    if not message.author.bot:
        await message.channel.send("hi")


@client.error
async def error_handler(error, coro) -> None:
    print(error)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(client.start(os.environ["BOT_TOKEN"]))
