import asyncio
from agents.coder import create_coder
from agents.debugger import create_debugger
from tools.python_executor import PythonExecutor
from tools.linter import PylintLinter
from groupchat.groupchat import RoundRobinGroupChat

async def main():
    user_task = input("📥 Enter your Python task: ")

    tools = [PythonExecutor(), PylintLinter()]
    coder = await create_coder(tools)
    debugger = await create_debugger(tools)

    chat = RoundRobinGroupChat([coder, debugger])
    await chat.run(user_task)

asyncio.run(main())
