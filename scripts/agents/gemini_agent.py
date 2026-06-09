import os
import json

from openai import OpenAI
from dotenv import load_dotenv

from .base_agent import BaseAgent

from prompt_template import PROMPT_TEMPLATE

load_dotenv()


class GeminiAgent(BaseAgent):

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def grade_essay(self, essay):

        prompt = PROMPT_TEMPLATE.format(
    essay=essay
)

        response = self.client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content.strip()

        if content.startswith("```"):

            lines = content.splitlines()

            if lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]

            content = "\n".join(lines).strip()

        try:
            result = json.loads(content)

        except json.JSONDecodeError:

            result = {
                "score": None,
                "feedback": content[:500]
            }

        return result