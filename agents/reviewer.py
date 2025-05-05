from crewai import Agent
from utils.openrouter_llm import ask_gpt

class ReviewerAgent:
    def __init__(self):
        self.role = "Reviewer"
        with open("prompts/reviewer.txt") as f:
            self.prompt_template = f.read()

    def run(self, papers):
        prompt = self.prompt_template.format(papers=papers)
        return ask_gpt(prompt)

