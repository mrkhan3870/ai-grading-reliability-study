import time
import pandas as pd

from agents.groq_agent import GroqAgent
from agents.gemini_agent import GeminiAgent
from agents.cerebras_agent import CerebrasAgent


df = pd.read_csv("data/processed/essays.csv")

df = df.sample(
    n=100,
    random_state=42
)

agents = {
    "groq": GroqAgent(),
    "gemini": GeminiAgent(),
    "cerebras": CerebrasAgent()
}

results = []

for _, row in df.iterrows():

    essay = row["essay"]

    row_result = {
        "essay_id": row["essay_id"],
        "human_score": row["human_score"]
    }

    for name, agent in agents.items():

        print(
            f"Essay {row['essay_id']} | {name}"
        )

        try:

            result = agent.grade_essay(essay)

            row_result[f"{name}_score"] = result.get("score")

            row_result[f"{name}_feedback"] = result.get(
                "feedback",
                ""
            )

        except Exception as e:

            print(e)

            row_result[f"{name}_score"] = None

            row_result[f"{name}_feedback"] = str(e)

        time.sleep(2)

    results.append(row_result)

results_df = pd.DataFrame(results)

results_df.to_csv(
    "results/tables/benchmark_results.csv",
    index=False
)

print(results_df.head())