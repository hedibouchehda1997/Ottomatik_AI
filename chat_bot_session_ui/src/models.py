
from .utils import load_env
import os
from openai import OpenAI

class GPTCall:
    def __init__(self, model: str, api_key: str, system_prompt: str = None):
        self.model = model
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=self.api_key)

    def __call__(self, human_message: str):
        messages = []
        if self.system_prompt is not None:

            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": human_message})

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        )

        # This is a generator: yields tokens as they arrive
        for chunk in stream:
            delta = getattr(chunk.choices[0].delta, 'content', None)
            if delta:
                yield delta

if    __name__ == "__main__":
    # Example CLI/streaming logic (not using streamlit here)
    prompt = input("Enter your prompt: ")
    with load_env(["OPENAI_API_KEY"]):
        key = os.environ.get("OPENAI_API_KEY")
        gpt_call = GPTCall(
            model="gpt-4",
            api_key=key,
        )
        print("Streaming response:\n")
        for token in gpt_call(prompt):
            print(token, end="", flush=True)
        print("\nDone.")

