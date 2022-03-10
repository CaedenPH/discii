# discii
A test discord wrapper.

> Example Client:
> ```py
> import asyncio
> import os
> import discii
> 
> from dotenv import load_dotenv
> 
> client = discii.Client()
> 
> 
> @client.on("READY")
> async def ready():
>     print("the client is connected and ready")
> 
> 
> @client.on("MESSAGE_CREATE")
> async def message(message: discii.Message):
>     print(message.content)
> 
> 
> if __name__ == "__main__":
>     load_dotenv()
>    asyncio.run(client.start(os.environ["BOT_TOKEN"]))
> ```