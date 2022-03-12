import os
import asyncio
import discii

from dotenv import load_dotenv

client = discii.Client()


@client.on("READY")
async def bot_ready() -> None:
    print("The bot is ready.")


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(client.start(os.environ["BOT_TOKEN"]))
