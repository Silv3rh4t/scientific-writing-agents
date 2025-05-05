
from crewai import Agent
from utils.openrouter_llm import ask_gpt

class ValidatorAgent:
    def __init__(self):
        self.role = "Validator"
        with open("prompts/validator.txt") as f:
            self.prompt_template = f.read()

    def run(self, scope, premise, hypothesis):
        prompt = self.prompt_template.format(scope=scope, premise=premise, hypothesis=hypothesis)
        return ask_gpt(prompt)
