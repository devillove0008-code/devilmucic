from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_USERNAME, OWNER_URL, CHANNEL_URL, SUPPORT_URL

def home_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "✚ ADD ME IN YOUR GROUP ✚",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
        )],
        [
            InlineKeyboardButton("≡ OWNER ≡", url=OWNER_URL),
            InlineKeyboardButton("≡ CHANNEL ≡", url=CHANNEL_URL),
        ],
        [InlineKeyboardButton("≡ SUPPORT ≡", url=SUPPORT_URL)]
    ])
