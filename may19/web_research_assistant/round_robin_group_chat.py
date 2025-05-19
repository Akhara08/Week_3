# round_robin_group_chat.py
class RoundRobinGroupChat:
    def __init__(self, agents):
        self.agents = agents
        self.current = 0  # index to keep track of whose turn it is

    async def chat(self, message):
        agent = self.agents[self.current]
        print(f"[RoundRobinGroupChat] Agent {agent.__class__.__name__} processing message...")
        response = await agent.process(message)
        self.current = (self.current + 1) % len(self.agents)
        return response
