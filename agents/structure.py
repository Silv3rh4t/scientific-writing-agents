import openai
import os
import json
import hashlib

# Simulated local cache (use persistent storage in production)
evidence_cache = {}

# Utility for caching keys
def cache_key(text):
    return hashlib.sha256(text.encode()).hexdigest()

class StructureAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-1106-preview"
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_core",
                    "description": "Search CORE academic API for research relevant to a point.",
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
                    "name": "search_web",
                    "description": "Perform a general web search to support an article point.",
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

    def run(self, user_input, previous_structure=None):
        """Generates an updated structure and adds evidence with caching."""
        cached_key = cache_key(user_input)
        if cached_key in evidence_cache:
            return evidence_cache[cached_key]

        system_prompt = (
            "You are a structuring and research agent. Your job is to take the user's input and convert it into:\n\n"
            "1. A structured list of 3–6 logically ordered points.\n"
            "2. For each point, search for 1 supporting research source, preferably from CORE or the web.\n"
            "3. Format your output strictly in JSON with keys: structure → points[], and evidence{}.\n"
            "4. Do not include any non-JSON content.\n"
            "5. You may call tools to assist your research if needed."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message

        if msg.get("tool_calls"):
            # Handle tool invocation round
            tool_outputs = []
            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                if tool_name == "search_core":
                    result = self._mock_core_search(args["query"])
                elif tool_name == "search_web":
                    result = self._mock_web_search(args["query"])
                else:
                    result = "No tool result"

                tool_outputs.append({
                    "role": "function",
                    "name": tool_name,
                    "content": result
                })

            # Add tool results and resume conversation
            messages.append(msg)
            messages.extend(tool_outputs)

            followup = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="none"
            )
            final_output = followup.choices[0].message.content
        else:
            final_output = msg.content

        try:
            parsed = json.loads(final_output)
            evidence_cache[cached_key] = parsed
            return parsed
        except Exception as e:
            return {
                "structure": {
                    "points": [],
                    "evidence": {}
                },
                "error": f"Parsing failed: {str(e)}",
                "raw_output": final_output
            }

    def _mock_core_search(self, query):
        # Replace with actual CORE API logic
        return json.dumps({
            "title": f"CORE result for {query}",
            "link": f"https://core.ac.uk/search?q={query}",
            "description": f"Simulated academic article supporting: {query}"
        })

    def _mock_web_search(self, query):
        # Replace with actual web search logic
        return json.dumps({
            "title": f"Web article on {query}",
            "link": f"https://example.com?q={query}",
            "description": f"Simulated web content supporting: {query}"
        })
