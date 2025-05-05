from crewai import Agent
from utils.openrouter_llm import ask_gpt

class CriticAgent:
    def __init__(self):
        self.role = "Critic"
        with open("prompts/critic.txt") as f:
            self.prompt_template = f.read()

    def run(self, draft):
        prompt = self.prompt_template.format(draft=draft)
        return ask_gpt(prompt)

