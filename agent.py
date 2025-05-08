import os
import json
import uuid
import requests
from datetime import datetime
from tools import core_search, tavily_search

class SpectreAgent:
    def __init__(self, system_prompt=None):
        self.model = "openai/gpt-4.1-nano"
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        if system_prompt:
            self.prompt = system_prompt
        else:
            with open("prompts/chat.txt") as f:
                self.prompt = f.read()

        self.history = []
        self.session_id = str(uuid.uuid4())
        self.article = {}  # for sidebar
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
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "tavily_search",
                    "description": "Search the web for recent content on a topic.",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
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

    def _record_cost(self, usage):
        self.token_in += usage.get("prompt_tokens", 0)
        self.token_out += usage.get("completion_tokens", 0)

    def _estimate_cost(self):
        return round((self.token_in * 0.10 + self.token_out * 0.40) / 1_000_000, 6)

    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        messages = [
            {"role": "system", "content": self.prompt},
            *[msg if isinstance(msg["content"], str) else {"role": msg["role"], "content": json.dumps(msg["content"])} for msg in self.history]
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "tools": self.tools,
            "tool_choice": "auto"
        }

        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=self._headers(), json=payload)
        if not r.ok:
            return {"chat": f"API Error: {r.status_code}", "side": {}}

        data = r.json()
        if "choices" not in data:
            return {"chat": f"Unexpected response: {json.dumps(data)}", "side": {}}

        msg = data["choices"][0]["message"]
        usage = data.get("usage", {})
        self._record_cost(usage)

        print("\n[GPT THOUGHT]:\n", json.dumps(msg, indent=2))

        tool_calls = []
        if "tool_calls" in msg:
            self.history.append(msg)
            for call in msg["tool_calls"]:
                name = call["function"]["name"]
                args = json.loads(call["function"]["arguments"])
                result = core_search(args["query"]) if name == "core_search" else tavily_search(args["query"])
                self.history.append({
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "name": name,
                    "content": result
                })
                tool_calls.append({"name": name, "arguments": args})
            return self.chat("(continue)")

        content = msg.get("content", {})
        parsed = {}
        if isinstance(content, str):
            try:
                parsed = json.loads(content)
            except Exception as e:
                print("[WARN] Failed to parse assistant content as JSON:", e)
                parsed = {"chat": content, "side": {}}
        else:
            parsed = {"chat": str(content), "side": {}}

        msg["content"] = json.dumps(parsed)
        self.history.append(msg)

        chat_text = parsed.get("chat", "")
        side_update = parsed.get("side", {})
        if isinstance(side_update, dict):
            self.article.update(side_update)

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "model_response": parsed,
            "tool_calls": tool_calls,
            "token_usage": {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total": usage.get("total_tokens", 0)
            },
            "model": self.model
        }
        os.makedirs("storage/logs", exist_ok=True)
        log_file = f"storage/logs/live_session_{self.session_id[:8]}.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        return {"chat": chat_text, "side": side_update}

    def get_article(self):
        return "\n\n".join(self.article.get(str(i), "") for i in sorted(map(int, self.article)))

    def export_session(self):
        os.makedirs("storage/logs", exist_ok=True)
        filename = f"storage/logs/session_{self.session_id[:8]}.json"
        with open(filename, "w") as f:
            json.dump({
                "session_id": self.session_id,
                "tokens_in": self.token_in,
                "tokens_out": self.token_out,
                "cost_usd": self._estimate_cost(),
                "messages": self.history,
                "article": self.article
            }, f, indent=2)
