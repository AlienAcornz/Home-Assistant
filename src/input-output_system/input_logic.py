import queue
import sounddevice as sd
import sys
import json
from vosk import Model, KaldiRecognizer
from pathlib import Path
from .output_logic import speak
import re
from ..prompt_system.response_logic import Agent

def clean_text(s: str) -> str:
    # allow letters and spaces, lowercase
    return re.sub(r'[^a-zA-Z\s]', '', s.lower()).strip()

llama = Agent()
assistant_reply = ""

# Locate and load Vosk model
project_root = Path(__file__).resolve().parents[2]
model_path = str(project_root / "assets" / "vosk-model-small")
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)
recognizer.SetWords(True)  # include word-level timing

audio_queue = queue.Queue()
is_speaking = False

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    # drop audio while TTS is playing
    if not is_speaking:
        audio_queue.put(bytes(indata))

with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback
    ) as stream:
    print("Say something (say exit to stop)…")
    speak("Hello, what can I do for you today?")
    try:
        while True:
            data = audio_queue.get()
            # Use partial to get interim recognition (helps with accuracy)
            partial = json.loads(recognizer.PartialResult()).get("partial", "")
            if partial:
                # (Optional) show partial for visual feedback:
                print(f"...interpreting: {partial}", end='\r')

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                user_input = result.get("text", "").strip()

                # ignore empty or echo of TTS
                if not user_input \
                   or clean_text(user_input) == clean_text(assistant_reply):
                    continue

                print(f"User: {user_input}")
                if "exit" in user_input.lower().split(" "):
                    break

                # pause recognition while speaking
                is_speaking = True
                assistant_reply = llama.generate_response(user_input)
                speak(assistant_reply)
                is_speaking = False

                print(f"Agent: {assistant_reply}")

    except KeyboardInterrupt:
        pass
