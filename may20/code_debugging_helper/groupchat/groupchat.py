import asyncio



class RoundRobinGroupChat:
    def __init__(self, agents):
        self.agents = agents
        self.history = []
        self.last_lint_score = None
        self.last_coder_output_empty_after_perfect_lint = False

    async def run(self, user_message):
        message = user_message
        print(f"\n🧑 User Prompt: {message}\n")

        for _ in range(4):  # 2 rounds between coder/debugger
            for agent in self.agents:
                print(f"\n[{agent['name']}]")
                response = await agent["fn"](message, self.history)
                
                # Check if this agent is the linter to update last lint score
                if agent['name'].lower() == 'pylintlinter' or 'linter' in agent['name'].lower():
                    # Extract lint score from the response text
                    score_match = re.search(r"rated at (\d+\.\d+)/10", response)
                    if score_match:
                        self.last_lint_score = float(score_match.group(1))
                    else:
                        self.last_lint_score = None
                
                # Check if this agent is the coder
                if agent['name'].lower() == 'coder':
                    # Detect empty code blocks in coder response:
                    # We consider empty if response has only an empty code block or no code content
                    
                    # A very simple heuristic:
                    # Check if response is a code block with no code, or only whitespace/newlines
                    code_block_match = re.search(r"```python\s*(.*?)```", response, re.DOTALL)
                    code_content = code_block_match.group(1).strip() if code_block_match else ''
                    
                    if self.last_lint_score == 10.0 and (code_content == '' or self.last_coder_output_empty_after_perfect_lint):
                        # Instead of printing empty code block, print a helpful message or skip
                        print("# No changes needed, code is perfect. Skipping empty code generation.")
                        self.last_coder_output_empty_after_perfect_lint = True
                        # Don't update message with empty code block, keep last message to avoid confusion
                        continue
                    else:
                        self.last_coder_output_empty_after_perfect_lint = False
                
                self.history.append((agent["name"], response))
                print(response)
                message = response  # pass the latest message to next agent
