import threading
from pathlib import Path
from queue import Queue, Empty
from .io_system.input_logic import SpeechRecognizer
from .io_system.output_logic import speak
from .prompt_system.response_logic import Agent

# Initialize components
agent = Agent()
recognizer = None
user_text_queue = Queue()
stop_event = threading.Event()

def close_application():
    stop_event.set()
    recognizer.stop()

# Called by SpeechRecognizer for each final transcript
def handle_user_input(text: str):
    if text.lower().strip() == "exit":
        close_application()
    else:
        user_text_queue.put(text)

# Worker thread to process queued user inputs
def process_user_inputs():
    global recognizer
    while not stop_event.is_set():
        try:
            text = user_text_queue.get(timeout=0.5)
        except Empty:
            continue
        # Pause STT during TTS
        recognizer.is_speaking.set()
        print(f"⮞ User said: {text}")
        assistant_reply = agent.generate_response(text)
        speak(assistant_reply)
        print(f"⮜ Assistant replied: {assistant_reply}")
        recognizer.is_speaking.clear()

if __name__ == "__main__":
    model_path = Path(__file__).resolve().parent.parent / "assets" / "vosk-model-large"
    recognizer = SpeechRecognizer(model_path, blocksize=4000, debug=True)

    # Start STT and processing threads
    recognizer.start_listening(handle_user_input)
    threading.Thread(target=process_user_inputs, daemon=True).start()

    print("Starting... say 'exit' to quit.")
    recognizer.is_speaking.set()
    speak("Hello, how can I assist you today?")
    recognizer.is_speaking.clear()

    # Keep main thread alive until exit
    stop_event.wait()
