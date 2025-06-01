from groq import Groq
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

prompt_system_dir = Path(__file__).parent
project_root = prompt_system_dir.parent.parent

data_path = prompt_system_dir / "system_prompt.txt"

with open(data_path, "r", encoding="utf-8") as f:
    DEFAULT_SYSTEM_PROMPT = f.read()

load_dotenv(Path(project_root / ".env"))

class Agent():
    def __init__(
            self, api_key: str = os.getenv("GROQ_API_KEY"),
            system_prompt: str = DEFAULT_SYSTEM_PROMPT,
            temperature: int = 0.7,
            model: str = "llama-3.3-70b-versatile",
            stream: bool = False,
            summarize_chat = True
            ):
        self.client = Groq(api_key=api_key)
        self.system_prompt = system_prompt
        self.temprature = temperature
        self.stream = stream
        self.model = model
        self.summarize_chat = summarize_chat

        self.chat_history = [
            {"role": "system", "content": self.system_prompt}
        ]

    def __get_response(self, messages):
        response = self.client.chat.completions.create(
            model= self.model,
            messages=messages,
            temperature=self.temprature,
            stream=self.stream
        )
        return response.choices[0].message.content

    def generate_response(self, user_input: str) -> str:
        self.chat_history.append({"role": "user", "content": user_input})
        assistant_reply = self.__get_response(self.chat_history)
        self.chat_history.append({"role": "assistant", "content": assistant_reply})

        if self.summarize_chat != True:
            return assistant_reply
        
        from chat_summarizer import count_tokens, get_chat_summary
        tokens = count_tokens(self.chat_history)
        print(tokens)
        if count_tokens(self.chat_history) > 500:
            self.chat_history = [
                {"role": "system", "content": self.system_prompt},
                {"role": "assistant", "content": f"Here’s what we’ve discussed so far: {get_chat_summary(self.chat_history)}"},
                *self.chat_history[-3:]
            ]
        return assistant_reply
    
