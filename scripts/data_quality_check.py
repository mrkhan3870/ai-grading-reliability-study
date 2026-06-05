import pandas as pd

df = pd.read_csv("data/processed/essays.csv")

print("Rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nHuman score statistics:")
print(df["human_score"].describe())

print("\nScore distribution:")
print(df["human_score"].value_counts().sort_index())