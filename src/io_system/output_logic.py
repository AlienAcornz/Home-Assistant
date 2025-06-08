import asyncio
import edge_tts
from playsound import playsound
from tempfile import NamedTemporaryFile
import os
from ..api_system.log_utils import add_log

VOICE = "en-GB-RyanNeural"
RATE = "+0%"

async def speak_async(message):
    print(f"[TTS] Speaking: {message}")
    add_log(f"[TTS] Speaking: {message}", tag="TTS")
    communicate = edge_tts.Communicate(text=message, voice=VOICE, rate=RATE)
    with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        await communicate.save(temp_file.name)
        temp_path = temp_file.name

    playsound(temp_path)
    os.remove(temp_path)
    print(f"[TTS] Done speaking.")

def speak(message):
    asyncio.run(speak_async(message))