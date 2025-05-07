import os
import json
import hashlib
import requests
from agents.structure_agent import StructureAgent
from agents.draft_agent import DraftAgent

class ChatAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = "deepseek/deepseek-r1:free"  # Adjust based on OpenRouter availability

        self.structure = {
            "points": [],
            "evidence": {}
        }
        self.tone_notes = ""

        self.structure_tool = {
            "type": "function",
            "function": {
                "name": "structure_agent",
                "description": "Convert user thoughts into a structured article outline with evidence.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_input": {"type": "string"},
                        "existing_structure": {"type": "object"}
                    },
                    "required": ["user_input", "existing_structure"]
                }
            }
        }

        self.draft_tool = {
            "type": "function",
            "function": {
                "name": "draft_agent",
                "description": "Use the current structure and tone to generate a first draft.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "structure": {"type": "array", "items": {"type": "string"}},
                        "tone_instructions": {"type": "string"}
                    },
                    "required": ["structure", "tone_instructions"]
                }
            }
        }

        self.tools = [self.structure_tool, self.draft_tool]

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://yourapp.com",  # Optional: required by OpenRouter
            "X-Title": "SpectreBot"
        }

    def handle(self, user_input: str) -> str:
        with open("prompts/chat.txt", "r") as f:
            system_prompt = f.read()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "tools": self.tools,
            "tool_choice": "auto"
        }

        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=self._headers(),
            json=payload
        )
        r.raise_for_status()
        data = r.json()

        msg = data["choices"][0]["message"]

        if "tool_calls" in msg:
            responses = []
            for call in msg["tool_calls"]:
                name = call["function"]["name"]
                args = json.loads(call["function"]["arguments"])

                if name == "structure_agent":
                    result = StructureAgent().run(
                        args["user_input"], args["existing_structure"]
                    )
                    self.structure = result["structure"]
                    tool_result = json.dumps(result)

                elif name == "draft_agent":
                    tool_result = DraftAgent().run(
                        args["structure"], args["tone_instructions"]
                    )
                else:
                    tool_result = "Unsupported tool."

                # Now complete the conversation after tool response
                messages.append(msg)
                messages.append({
                    "role": "function",
                    "name": name,
                    "content": tool_result
                })

                followup = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=self._headers(),
                    json={
                        "model": self.model,
                        "messages": messages,
                        "tool_choice": "none"
                    }
                )
                followup.raise_for_status()
                return followup.json()["choices"][0]["message"]["content"].strip()

        return msg["content"].strip()

    def set_tone(self, tone: str):
        self.tone_notes = tone
