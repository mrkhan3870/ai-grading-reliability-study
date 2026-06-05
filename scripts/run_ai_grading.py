import os
import json
import time
import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

df = pd.read_csv("data/processed/essays.csv")
df = df.sample(n=100, random_state=42)  # reproducible random sample

results = []

for _, row in df.iterrows():

    essay = row["essay"]

    prompt = f"""You are an experienced writing assessor for high school argumentative essays.

Score this essay from 2 to 12.

SCORE DISTRIBUTION (based on 1,783 graded essays):
- 2-4: ~15% (seriously flawed)
- 5-7: ~30% (below average)
- 8-10: ~40% (average to good — MOST COMMON)
- 11-12: ~15% (excellent)

IMPORTANT: The majority of essays receive scores between 8-10. Do not inflate low scores.

Evaluate:
- Organization
- Argument quality
- Evidence
- Grammar
- Overall effectiveness

Return ONLY raw JSON: {{"score": integer, "feedback": "short feedback"}}

Essay:

{essay}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
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
        result = {"score": None, "feedback": content[:500]}

    results.append({
        "essay_id": row["essay_id"],
        "human_score": row["human_score"],
        "ai_score": result.get("score"),
        "ai_feedback": result.get("feedback", "")
    })

    time.sleep(2)

results_df = pd.DataFrame(results)
results_df.to_csv("results/tables/ai_scores_pilot.csv", index=False)
print(results_df)