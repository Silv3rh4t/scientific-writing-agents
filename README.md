# 🧠 GPT-4.1 Article Architect

A personal assistant for structuring and drafting thought-driven opinion pieces using GPT-4.1 via OpenRouter, built with a focus on prompt engineering and agent orchestration design.

This tool was built as an experiment in constructing a lean, dynamic agent-driven writing pipeline where the LLM handles both structured reasoning and iterative drafting in a conversational interface — while minimizing token costs and maintaining full control over the sidebar output.

---

## ✨ Features

- **Conversational Input** — Input your thoughts naturally, no form fields or rigid templates.
- **Dynamic Structure Agent** — Your thoughts are turned into a working structure that is continuously refined.
- **Smart Drafting** — Once ready, the agent begins drafting the article paragraph-wise and sends updates only when necessary.
- **Live Sidebar** — The sidebar reflects the evolving structure or working draft in real time.
- **Evidence-Backed Writing** — GPT optionally uses search tools (Tavily + CORE) to pull supporting material and validate reasoning.
- **Token Cost Tracker** — Shows tokens used and estimated session cost (based on OpenRouter pricing).
- **Session Logs** — Every interaction and article version is saved as a JSONL and exportable.

---

## ⚙️ Tech Stack

- **LLM API:** `openai/gpt-4.1-nano` via [OpenRouter](https://openrouter.ai)
- **Frontend:** Streamlit 
- **Architecture:** Tool-calling agent logic with system prompt control
- **Search tools:** Tavily API + CORE for academic research
- **Logging:** Token tracking, cost estimation, and full session history

---

## 🧪 Why This Exists

This project is part of an ongoing exploration into:
- Practical prompt engineering for tool-using agents
- Hybrid LLM architecture (chat + structure)
- Cost-aware writing systems that minimize context waste
- Designing a conversational frontend that feels intuitive but leverages agent reasoning underneath

---

## 🗂 Folder Structure

```
├── app.py                # Streamlit frontend
├── agent.py              # Core orchestrator logic
├── tools.py              # Search tools (Tavily, CORE)
├── prompts/chat.txt      # System prompt for chat agent
├── storage/logs/         # All session logs and history
```

---


## 🧠 Example Use Case

> Input: *“I believe the instability in Asia benefits the US warmachine. I want to argue for a Co-Prosperity Circle in Asia...”*

The agent:
- Structures this into a logical article outline
- Pulls evidence from academic and web sources
- Drafts a paragraph at a time into the sidebar
- Asks clarifying questions in the chat
- Saves everything you do

---

## 👨‍💻 Author

Built and maintained by [Akhand Yaduvanshi](https://hustlegrad.org), as part of ongoing research into LLM tooling and writing automation.