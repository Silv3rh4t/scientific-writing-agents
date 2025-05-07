from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class DraftAgent:
    def __init__(self):
        self.model = "gpt-4-1106-preview"

    def run(self, structure, tone_instructions):
        """
        Generate a full draft using structure + tone prompt passed by ChatAgent.
        """
        # Build the base prompt
        outline_str = "\n".join([f"- {point}" for point in structure])

        system_prompt = (
            "You are a professional opinion columnist. "
            "Use the provided outline to write a compelling, well-structured article. "
            "Incorporate transitions, persuasive flow, and a clear voice.\n"
            "The tone and style are defined by the user’s notes."
        )

        user_prompt = (
            f"Tone/style notes: {tone_instructions or 'neutral'}\n\n"
            f"Here is the outline:\n{outline_str}\n\n"
            "Please write the full article based on this."
        )

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        return response.choices[0].message.content.strip()
