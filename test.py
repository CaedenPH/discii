import os
import asyncio
import discii

from dotenv import load_dotenv


client = discii.Client()

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(client.start(os.environ["BOT_TOKEN"]))
