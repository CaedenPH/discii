<div align='center'>
  <img src = "assets/discii.png" width = "200" height="200">
  <br>

  `discii` - the lightweight discord wrapper.

  <br>
</div>

*If you have any features you would like me to implement make sure to make a pull request, an issue, or contact me on discord.*

**Example Client:**
> ```py
> import os
> import asyncio
> import discii
>
> from dotenv import load_dotenv
>
> client = discii.Client()
>
>
> @client.on("READY")
> async def bot_ready() -> None:
>     print(f"The client is ready. The client's latency is {round(client.latency * 1000)}s")
>
> @client.on("MESSAGE_CREATE")
> async def on_message(message: discii.Message):
>     print(f"Message detected. Message text: {message.text}")
>
>     embed = discii.Embed(title="Hello, this is the TITLE.", timestamp=message.timestamp, colour=0xfffff)
>     embed.add_field(name="Hello, I am a field!", value="I am a field value!")
>     embed.set_author(name="My name is Discii!")
>
>     if not message.author.bot:
>         m = await message.reply(embeds=[embed])
>         print([embed._to_dict() for embed in m.embeds])
>
>     test_channel = client.get_channel(953049224516370493)
>     if test_channel is not None:
>         await test_channel.send("Heyo!")
>
>     message = await message.author.send("hello.")
>     await message.edit("hello...")
>
>     user = client.get_user(928410016602525707)
>     if user is not None:
>         await message.guild.ban(user.id)
>
> @client.on("MESSAGE_DELETE")
> async def message_delete(message: discii.Message):
>    print(message)
>
> @client.error()
> async def event_error(error, coro) -> None:
>    print(error, coro)
>
> if __name__ == "__main__":
>     load_dotenv()
>     asyncio.run(client.start(os.environ["BOT_TOKEN"]))
> ```

**Example Bot**:
> ```py
> import os
> import asyncio
>
> from dotenv import load_dotenv
> from discii import commands
>
> bot = commands.Bot(prefixes=["."])
>
>
> @bot.command(names=["ping"])
> async def ping(context: commands.Context):
>     await context.send(f"The bots ping is **{round(bot.latency*1000)}**")
>
>
> @bot.command(names=["add"])
> async def add(context: commands.Context, num1: int, num2: int):
>     await context.send(f"{num1 + num2 = }")
>
> @bot.error(command=True)
> async def command_error(context: commands.Context, error):
>     print(context, error)
>
> if __name__ == "__main__":
>     load_dotenv()
>     asyncio.run(bot.start(os.environ["BOT_TOKEN"]))
> ```

**Event list**:
- `READY`
  args: `None`
- `MESSAGE_CREATE`
  args: `discii.Message`
- `MESSAGE_DELETE`
  args: `discii.Message`
- `error`
  args: `Any`, `typing.Coroutine`