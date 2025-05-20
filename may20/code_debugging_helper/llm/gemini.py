import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro-latest")

async def generate_response(prompt: str) -> str:
    response = await model.generate_content_async(prompt)
    return response.text
