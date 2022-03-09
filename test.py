import asyncio
import os
import disci

from dotenv import load_dotenv

client = disci.Client()

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(client.start(os.environ["BOT_TOKEN"]))