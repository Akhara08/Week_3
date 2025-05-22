import asyncio
from handler import handle_query

async def chatbot():
    print("Welcome to the FAQ Chatbot (RAG powered). Type 'exit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = await handle_query(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    asyncio.run(chatbot())