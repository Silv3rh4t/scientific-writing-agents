from utils.openrouter_llm import ask_gpt

class StructureAgent:
    def __init__(self):
        with open("prompts/structure_init.txt") as f:
            self.initial_prompt = f.read()
        with open("prompts/structure_discuss.txt") as f:
            self.discuss_prompt = f.read()
        self.memory = []

    def start(self, user_input):
        prompt = self.initial_prompt.format(thoughts=user_input)
        self.memory = [{"role": "user", "content": prompt}]
        response = ask_gpt(self.memory, max_tokens=1000)
        
        self.memory.append({"role": "assistant", "content": response})
        points = self._extract_points(response)
        return response, points

    def chat(self, user_msg):
        """Continue discussion to refine structure."""
        self.memory.append({"role": "user", "content": user_msg})
        response = ask_gpt(self.memory, max_tokens=1000)
        self.memory.append({"role": "assistant", "content": response})
        points = self._extract_points(response)
        return response, points

    def _extract_points(self, text):
        lines = text.splitlines()
        return [line.lstrip("- ").strip() for line in lines if line.startswith("- ")]
