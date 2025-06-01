import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150) 
engine.say(" ")
engine.runAndWait()
engine.stop()

def speak(message):
    engine.stop()
    engine.say(f"   {message}")
    engine.runAndWait()