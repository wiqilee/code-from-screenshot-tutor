import os

class LLMBackend:
    def __init__(self):
        self.backend = os.environ.get("LLM_BACKEND", "openai")
        self.model_id = os.environ.get("LLM_MODEL_ID", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    def generate(self, prompt: str) -> str:
        if self.backend == "openai":
            from openai import OpenAI
            client = OpenAI()
            res = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}])
            return res.choices[0].message.content
        else:
            from transformers import pipeline
            pipe = pipeline("text-generation", model=self.model_id, device=-1)
            out = pipe(prompt, max_new_tokens=256)
            return out[0]["generated_text"]
