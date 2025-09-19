# mock_agent.py

from agents import Agent, Runner

class MockRunner(Runner):
    @staticmethod
    def run_sync(agent, prompt):
        class Result:
            def __init__(self, output):
                self.final_output = output
        # Instead of calling OpenAI, we just return a fixed string, no 'quota' left.
        return Result(f"Simulated response for prompt: '{prompt}'")

# Create an agent (instructions won't matter for mock)
agent = Agent(name="Assistant", instructions="You are a helpful assistant.")

# Use MockRunner instead of real Runner
result = MockRunner.run_sync(agent, "Say hello world without using API quota")
print(result.final_output)