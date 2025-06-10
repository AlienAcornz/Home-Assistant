from groq import Groq, RateLimitError
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
import json
from .tools.select_tool_logic import select_tool
from ..api_system.log_utils import add_log

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
        self.temperature = temperature
        self.stream = stream
        self.model = model
        self.summarize_chat = summarize_chat

        self.chat_history = [
            {"role": "system", "content": self.system_prompt}
        ]

    def __get_response(self, messages):
        try:
            response = self.client.chat.completions.create(
                model= self.model,
                messages=messages,
                temperature=self.temperature,
                stream=self.stream
            )
            return response.choices[0].message.content
        except RateLimitError:
            add_log("Rate limit reached!", tag="error")
            return '{"response": "I am currently experiencing high demand. Please try again in a moment.", "action": {}}'
        

    def generate_response(self, user_input: str, role="user") -> str:
        self.chat_history.append({"role": role, "content": user_input})
        assistant_reply_raw = self.__get_response(self.chat_history)
        self.chat_history.append({"role": "assistant", "content": assistant_reply_raw})

        try :
            assistant_reply = json.loads(assistant_reply_raw)
            response_text = assistant_reply.get("response", assistant_reply_raw)

            actions = assistant_reply.get("action", {})
            response_text = select_tool(actions, response_text)
        except json.JSONDecodeError:
            add_log("Could not read message format!", tag="error")
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
    
