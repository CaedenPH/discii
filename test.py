import asyncio
import os
import disci

from dotenv import load_dotenv

client = disci.Client()


@client.on("READY")
async def ready(raw_data):
    print("the client is connected and ready")


@client.on("MESSAGE_CREATE")
async def message(message: disci.Message):
    print(message.content)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(client.start(os.environ["BOT_TOKEN"]))
