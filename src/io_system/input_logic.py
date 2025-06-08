import threading
import queue
import sounddevice as sd
import sys
import json
from vosk import Model, KaldiRecognizer
from pathlib import Path
from ..api_system.log_utils import add_log

class SpeechRecognizer:
    def __init__(self,
                 model_dir: Path,
                 sample_rate: int = 16000,
                 blocksize: int = 4000,
                 debug: bool = False):
        self.sample_rate = sample_rate
        self.blocksize = blocksize
        self.audio_queue = queue.Queue()
        self.is_speaking = threading.Event()
        self.debug = debug

        # Load and initialize Vosk model
        self.model = Model(str(model_dir))
        self._init_recognizer()

        # Thread control
        self._thread = None
        self._stop_event = threading.Event()

    def _init_recognizer(self):
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
        self.recognizer.SetWords(True)
        if self.debug:
            print("Recognizer initialized")
            add_log(message ="Recognizer initialized", tag="STT")

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        if not self.is_speaking.is_set():
            pcm = bytes(indata)
            self.audio_queue.put(pcm)

    def _recognize_loop(self, on_result):
        try:
            while not self._stop_event.is_set():
                chunk = self.audio_queue.get()
                if self.recognizer.AcceptWaveform(chunk):
                    res = json.loads(self.recognizer.Result())
                    text = res.get("text", "").strip()
                    if text:
                        if self.debug:
                            print(f"[Debug] Final result: {text}")
                            add_log(message=f"Final result: {text}", tag="STT")
                        on_result(text)
                    # Reset recognizer and clear backlog
                    self._init_recognizer()
                    while not self.audio_queue.empty():
                        try:
                            self.audio_queue.get_nowait()
                        except queue.Empty:
                            break
                else:
                    if self.debug:
                        partial = json.loads(self.recognizer.PartialResult()).get("partial")
                        if partial:
                            print(f"Interpreting: {partial}")
        except Exception as e:
            add_log(f"[Error in recognition loop] {e}", tag="error")
            print(f"[Error in recognition loop] {e}", file=sys.stderr)

    def start_listening(self, on_result):
        # Launch recognition thread
        self._thread = threading.Thread(
            target=self._recognize_loop,
            args=(on_result,),
            daemon=True
        )
        self._thread.start()

        # Start audio capture
        self._stream = sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=self.blocksize,
            dtype='int16',
            channels=1,
            callback=self._audio_callback
        )
        self._stream.start()
        if self.debug:
            add_log("Audio stream started", tag="STT")
            print("[Debug] Audio stream started")

    def stop(self):
        self._stop_event.set()
        try:
            self._stream.stop()
            self._stream.close()
        except Exception:
            pass
        if self._thread:
            self._thread.join()
