import asyncio
import google.generativeai as genai

# Replace with your actual Gemini API key
genai.configure(api_key="AIzaSyDxsZ7llhXOT9HzG9bCPZ4p0xGxBEMNYAQ")
model = genai.GenerativeModel("gemini-1.5-pro-latest")

async def generate_answer(prompt):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
    return response.text.strip()
