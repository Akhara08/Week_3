from llm.gemini import generate_response

async def create_coder(tools):
    async def coder_fn(message, history):
        response = await generate_response(f"You are a Python coder. User asked: {message}\nRespond with working Python code only.")
        return response
    return {"name": "Coder 🧠", "tools": tools, "fn": coder_fn}
