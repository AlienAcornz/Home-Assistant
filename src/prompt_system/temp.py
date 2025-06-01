import response_logic

import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150) 
engine.say(" ")
engine.runAndWait()
engine.stop()

llama = response_logic.Agent()
print("Chat with Llama (type 'exit' to quit)")
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break
    assistant_reply = llama.generate_response(user_input)
    print(f"llama:{assistant_reply}")
    engine.stop()
    engine.say(f"   {assistant_reply}")
    engine.runAndWait()
