import aiohttp
import asyncio
import json
import disci

from disci.utils import _to_json
from constants import GATEWAY_URL, IDENTIFY_PAYLOAD

async def main():
    session = aiohttp.ClientSession()
    ws = await session.ws_connect(GATEWAY_URL)
    await ws.send_str(_to_json(IDENTIFY_PAYLOAD))

    num = 0
    while True:
        msg = await ws.receive()
        num += 1
        print(msg)
        msg_json = json.loads(msg.data)

        # if num == 4:
        #     return await session.close()
        if msg_json["t"] == "GUILD_CREATE":
            num -= 1
            continue

        # print(str(msg_json) + "\n\n\n\n")

        if msg.type is aiohttp.WSMsgType.CLOSE:
            print(str(msg) + " :(")
        if msg.type is aiohttp.WSMsgType.CLOSED:
            return


if __name__ == "__main__":
  asyncio.run(main())