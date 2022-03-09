import os
from dotenv import load_dotenv

load_dotenv()

GATEWAY_URL = "wss://gateway.discord.gg/?v=9&encoding=json"
IDENTIFY_PAYLOAD = {
  "op": 2,
  "d": {
      "token": os.environ["BOT_TOKEN"],
      "intents": 513,
      "properties": {
          "$os": "linux",
          "$browser": "my_library",
          "$device": "my_library",
      },
  },
}