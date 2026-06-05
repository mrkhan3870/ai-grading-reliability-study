import pandas as pd

# --------------------------------------------------
# Load raw dataset
# --------------------------------------------------

df = pd.read_csv(
    "data/raw/training_set_rel3.tsv",
    sep="\t",
    encoding="latin1"
)

print(f"Original dataset size: {len(df)} essays")

# --------------------------------------------------
# Keep only Essay Set 1
# --------------------------------------------------

df = df[df["essay_set"] == 1]

print(f"After filtering Essay Set 1: {len(df)} essays")

# --------------------------------------------------
# Keep only columns needed for the study
# --------------------------------------------------

df = df[
    [
        "essay_id",
        "essay",
        "domain1_score"
    ]
]

# --------------------------------------------------
# Rename column for clarity
# --------------------------------------------------

df = df.rename(
    columns={
        "domain1_score": "human_score"
    }
)

# --------------------------------------------------
# Check for missing values
# --------------------------------------------------

missing_values = df.isnull().sum()

print("\nMissing values:")
print(missing_values)

# --------------------------------------------------
# Remove rows with missing values
# --------------------------------------------------

df = df.dropna()

print(f"\nAfter removing missing values: {len(df)} essays")

# --------------------------------------------------
# Randomly sample 100 essays
# --------------------------------------------------

df = df.sample(
    n=100,
    random_state=42
)

# --------------------------------------------------
# Sort by essay_id
# --------------------------------------------------

df = df.sort_values(
    by="essay_id"
)

# --------------------------------------------------
# Save processed dataset
# --------------------------------------------------

output_path = "data/processed/essays.csv"

df.to_csv(
    output_path,
    index=False
)

print(f"\nSaved {len(df)} essays")
print(f"Output file: {output_path}")