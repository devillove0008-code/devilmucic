from pytgcalls.types.input_stream import InputStream, AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
from bot.app import call
from music.queue import joined

def stream(src):
    return InputStream(AudioPiped(src), HighQualityAudio())

async def join_or_change(chat_id, src):
    if not joined.get(chat_id):
        await call.join_group_call(chat_id, stream(src))
        joined[chat_id] = True
    else:
        await call.change_stream(chat_id, stream(src))
