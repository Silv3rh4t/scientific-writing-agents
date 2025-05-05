from crewai import Agent
from utils.openrouter_llm import ask_gpt

class SearcherAgent:
    def __init__(self):
        self.role = "Searcher"
        with open("prompts/searcher.txt") as f:
            self.prompt_template = f.read()

    def run(self, hypothesis):
        prompt = self.prompt_template.format(hypothesis=hypothesis)
        return ask_gpt(prompt)

