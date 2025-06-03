from groq import Groq
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
import json
from tools import time_utils

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
        assistant_reply_raw = self.__get_response(self.chat_history)
        self.chat_history.append({"role": "assistant", "content": assistant_reply_raw})

        try :
            assistant_reply = json.loads(assistant_reply_raw)
            response_text = assistant_reply.get("response", assistant_reply_raw)

            actions = assistant_reply.get("action", {})
            for action_name, params in actions.items():
                match action_name:
                    case "set_timer":
                        time_utils.set_timer(int(params[0]))
                    case "get_timer":
                        if params:
                            time_utils.get_timer(int(params[0]))
                        else:
                            time_utils.get_timer()
                    case "reset_timer":
                        if params:
                            time_utils.reset_timer(int(params[0]))
                        else:
                            time_utils.reset_timer()
                    case _:
                        print(f"Action: {action_name} not found!")
        except json.JSONDecodeError:
            response_text = assistant_reply_raw

        if self.summarize_chat != True:
            return response_text
        
        from .chat_summarizer import count_tokens, get_chat_summary
        tokens = count_tokens(self.chat_history)
        if count_tokens(self.chat_history) > 500:
            self.chat_history = [
                {"role": "system", "content": self.system_prompt},
                {"role": "assistant", "content": f"Here’s what we’ve discussed so far: {get_chat_summary(self.chat_history)}"},
                *self.chat_history[-3:]
            ]
        return response_text
    
