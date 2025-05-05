from crewai import Agent
from utils.openrouter_llm import ask_gpt

class DrafterAgent:
    def __init__(self):
        self.role = "Drafter"
        with open("prompts/drafter.txt") as f:
            self.prompt_template = f.read()

    def run(self, scope, hypothesis, review):
        prompt = self.prompt_template.format(scope=scope, hypothesis=hypothesis, review=review)
        return ask_gpt(prompt, max_tokens=3000)

