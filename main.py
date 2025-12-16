import asyncio
from pyrogram import filters
from bot.app import app, call
from bot.ui import home_kb
from music.youtube import yt_download
from music.queue import queue, now_playing, joined
from music.player import join_or_change

WELCOME = (
    "🎧 <b>GROUP VC MUSIC BOT</b>\n\n"
    "Use: <code>/play song name</code>\n"
    "Voice Chat ON hona chahiye"
)

@app.on_message(filters.command("start"))
async def start(_, m):
    await m.reply_text(WELCOME, reply_markup=home_kb(), parse_mode="html")

@app.on_message(filters.command("play") & filters.group)
async def play(_, m):
    chat = m.chat.id
    if len(m.command) < 2:
        return await m.reply_text("❌ Use: /play song name")

    await m.reply_text("🔎 Searching & downloading...")
    audio = yt_download(" ".join(m.command[1:]))

    if not audio:
        return await m.reply_text("❌ Song not found")

    if not now_playing.get(chat):
        now_playing[chat] = audio
        await join_or_change(chat, audio)
        await m.reply_text("▶️ Playing")
    else:
        queue.setdefault(chat, []).append(audio)
        await m.reply_text(f"➕ Added to queue ({len(queue[chat])})")

@app.on_message(filters.command("pause") & filters.group)
async def pause(_, m):
    await call.pause_stream(m.chat.id)
    await m.reply_text("⏸ Paused")

@app.on_message(filters.command("resume") & filters.group)
async def resume(_, m):
    await call.resume_stream(m.chat.id)
    await m.reply_text("▶️ Resumed")

@app.on_message(filters.command("skip") & filters.group)
async def skip(_, m):
    chat = m.chat.id
    if queue.get(chat):
        nxt = queue[chat].pop(0)
        now_playing[chat] = nxt
        await join_or_change(chat, nxt)
        await m.reply_text("⏭ Skipped")
    else:
        await call.leave_group_call(chat)
        joined[chat] = False
        now_playing[chat] = None
        await m.reply_text("⏹ Stopped")

@app.on_message(filters.command("stop") & filters.group)
async def stop(_, m):
    chat = m.chat.id
    await call.leave_group_call(chat)
    joined[chat] = False
    now_playing[chat] = None
    queue[chat] = []
    await m.reply_text("⏹ Stopped")

@call.on_stream_end()
async def auto_next(_, upd):
    chat = upd.chat_id
    if queue.get(chat):
        nxt = queue[chat].pop(0)
        now_playing[chat] = nxt
        await join_or_change(chat, nxt)
    else:
        await call.leave_group_call(chat)
        joined[chat] = False
        now_playing[chat] = None

async def main():
    await app.start()
    await call.start()
    print("✅ MUSIC BOT RUNNING")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
