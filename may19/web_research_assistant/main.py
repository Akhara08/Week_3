# main.py
import asyncio
from researcher import Researcher
from summarizer import Summarizer
from round_robin_group_chat import RoundRobinGroupChat

async def main():
    researcher = Researcher()
    summarizer = Summarizer()

    group_chat = RoundRobinGroupChat([researcher, summarizer])

    url = input("Enter URL to research: ")

    # Researcher fetches the content
    fetched_content = await group_chat.chat(url)

    if not fetched_content:
        print("Failed to fetch content.")
        return

    # Summarizer summarizes the fetched content
    summary = await group_chat.chat(fetched_content)

    print("\n--- Summary ---")
    print(summary)

if __name__ == "__main__":
    asyncio.run(main())
