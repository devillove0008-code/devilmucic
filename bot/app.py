from pyrogram import Client
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "vc_music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call = PyTgCalls(app)
