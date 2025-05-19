# summarizer.py
from llm import GeminiLLM

class Summarizer:
    def __init__(self):
        self.llm = GeminiLLM()

    async def process(self, text: str) -> str:
        print("[Summarizer] Summarizing content...")
        summary = await self.llm.summarize(text)
        print("[Summarizer] Summary complete")
        return summary
