import pandas as pd

# Load dataset
df = pd.read_csv(
    "data/raw/training_set_rel3.tsv",
    sep="\t",
    encoding="latin1"
)

print("\n=== First 5 Rows ===")
print(df.head())

print("\n=== Columns ===")
print(df.columns.tolist())

print("\n=== Shape ===")
print(df.shape)

print("\n=== Essay Sets ===")
print(df["essay_set"].value_counts().sort_index())

print("\n=== Score Ranges By Essay Set ===")
print(
    df.groupby("essay_set")["domain1_score"]
      .agg(["min", "max", "mean", "count"])
)