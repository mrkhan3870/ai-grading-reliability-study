import pandas as pd

from agents.groq_agent import GroqAgent


agent = GroqAgent()

df = pd.read_csv(
    "data/processed/essays.csv"
)

essay = df.iloc[0]["essay"]

result = agent.grade_essay(essay)

print(result)