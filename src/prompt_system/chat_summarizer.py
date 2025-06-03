import tiktoken
from .response_logic import Agent

def count_tokens(messages, model="gpt-3.5-turbo"):
    enc = tiktoken.encoding_for_model(model)
    total = 0
    for msg in messages:
        total += len(enc.encode(msg["content"]))
    return total

def get_chat_summary(chat_history):
    system_prompt = (
        "Summarize the following chat history in a few sentences. "
        "Your response must be in the following JSON format:\n\n"
        "{\n"
        '  "response": "RESPONSE HERE",\n'
        '  "action": {}\n'
        "}"
    )
    agent = Agent(system_prompt=system_prompt, summarize_chat=False)
    summarized_history = agent.generate_response(str(chat_history.pop(0)))
    return summarized_history