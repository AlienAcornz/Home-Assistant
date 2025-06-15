import threading
from pathlib import Path
from queue import Queue, Empty
from .io_system.input_logic import SpeechRecognizer
from .io_system.output_logic import speak
from .prompt_system.response_logic import Agent
from .api_system.log_utils import add_log
from .prompt_system.tools.time_utils import stop_alarm, check_alarm, get_active_state
import time
prev_response_time = time.time()

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
    global recognizer
    print(get_active_state())
    if text and get_active_state():
        recognizer.is_speaking.set()
        stop_alarm()
        speak("The alarm was stopped.")
        recognizer.is_speaking.clear()
        return 0
    if text.lower().strip() == "exit":
        add_log("Termination word detected!", tag="system")
        close_application()
    else:
        user_text_queue.put(text)

# Worker thread to process queued user inputs
def process_user_inputs():
    global recognizer
    global prev_response_time
    while not stop_event.is_set():
        check_alarm()
        try:
            text = user_text_queue.get(timeout=0.5)
        except Empty:
            continue
        # Pause STT during TTS

        if "milo" in text.lower() or prev_response_time + 30 >= time.time():
            prev_response_time = time.time()
            recognizer.is_speaking.set()
            add_log(f"⮞ User said: {text}", tag="chat")

            assistant_reply = agent.generate_response(text)
            speak(assistant_reply)
            add_log(f"⮜ Assistant replied: {assistant_reply}", tag="chat")
            recognizer.is_speaking.clear()

if __name__ == "__main__":
    model_path = Path(__file__).resolve().parent.parent / "assets" / "vosk-model-large"
    recognizer = SpeechRecognizer(model_path, blocksize=4000, debug=True)

    # Start STT and processing threads
    recognizer.start_listening(handle_user_input)
    threading.Thread(target=process_user_inputs, daemon=True).start()

    print("Starting... say 'exit' to quit.")
    add_log(message="Starting system...", tag="system")
    recognizer.is_speaking.set()
    speak("Hello, how can I assist you today?")
    recognizer.is_speaking.clear()

    # Keep main thread alive until exit
    stop_event.wait()
