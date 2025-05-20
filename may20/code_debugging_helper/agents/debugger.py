from llm.gemini import generate_response

async def create_debugger(tools):
    async def debugger_fn(message, history):
        result_messages = []
        for tool in tools:
            tool_result = await tool.run(message)
            result_messages.append(f"[{tool.name}]\n{tool_result}")
        return "\n".join(result_messages)
    return {"name": "Debugger 🛠", "tools": tools, "fn": debugger_fn}
