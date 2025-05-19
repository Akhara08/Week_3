# llm.py
import os
import asyncio
import google.generativeai as genai

class GeminiLLM:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError("GOOGLE_API_KEY not set in environment")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro-latest")

    async def summarize(self, text: str) -> str:
        loop = asyncio.get_event_loop()
        prompt = f"Summarize the following content concisely:\n\n{text[:8000]}"
        response = await loop.run_in_executor(None, lambda: self.model.generate_content(prompt))
        return response.text.strip()
