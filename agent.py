import os
import json
import uuid
import requests
from datetime import datetime
from tools import core_search, web_search

class SpectreAgent:
    def __init__(self, system_prompt):
        self.model = "openai/gpt-4.1-nano"
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        self.prompt = system_prompt
        self.history = []
        self.sidebar = ""
        self.sidebar_snapshots = []
        self.session_id = str(uuid.uuid4())

        self.token_in = 0
        self.token_out = 0

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "core_search",
                    "description": "Search academic papers on a topic.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search the web for recent content on a topic.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                }
            }
        ]

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://yourapp.com",
            "X-Title": "SpectreBot"
        }

    def _record_cost(self, input_tokens, output_tokens):
        self.token_in += input_tokens
        self.token_out += output_tokens

    def _estimate_cost(self):
        in_cost = self.token_in * 0.10 / 1_000_000
        out_cost = self.token_out * 0.40 / 1_000_000
        return round(in_cost + out_cost, 6)

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": self.prompt}] + self.history

        payload = {
            "model": self.model,
            "messages": messages,
            "tools": self.tools,
            "tool_choice": "auto"
        }

        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=self._headers(), json=payload)
        data = r.json()
        msg = data["choices"][0]["message"]

        self._record_cost(data["usage"]["prompt_tokens"], data["usage"]["completion_tokens"])

        if "tool_calls" in msg:
            for call in msg["tool_calls"]:
                tool = call["function"]["name"]
                args = json.loads(call["function"]["arguments"])
                if tool == "core_search":
                    result = core_search(args["query"])
                elif tool == "web_search":
                    result = web_search(args["query"])
                else:
                    result = "Tool not recognized."

                self.history.append(msg)
                self.history.append({
                    "role": "function",
                    "name": tool,
                    "content": result
                })

                return self.chat("(continue)")

        self.history.append(msg)
        content = msg["content"]

        if "===SIDEBAR===" in content:
            chat, sidebar = content.split("===SIDEBAR===")
            self.sidebar = sidebar.strip()
            self.sidebar_snapshots.append({
                "time": datetime.now().isoformat(),
                "content": self.sidebar
            })
            return chat.strip()
        return content.strip()

    def export_session(self):
        from storage.session_log import save_session
        save_session(self.session_id, {
            "messages": self.history,
            "sidebar": self.sidebar_snapshots,
            "tokens_in": self.token_in,
            "tokens_out": self.token_out,
            "cost_usd": self._estimate_cost()
        })

    def replace_paragraph(self, old_text, new_paragraph):
        """Future: Only submit and re-write one part of article to save cost"""
        lines = self.sidebar.split("\n\n")
        updated = [new_paragraph if old_text in para else para for para in lines]
        self.sidebar = "\n\n".join(updated)
