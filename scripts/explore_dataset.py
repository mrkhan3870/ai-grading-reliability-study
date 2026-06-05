import pandas as pd

# Load dataset
df = pd.read_csv(
    "data/raw/training_set_rel3.tsv",
    sep="\t",
    encoding="latin1"
)

print("\n=== First 5 Rows ===")
print(df.head()) #to check if dataset was loaded properly

print("\n=== Columns ===")
print(df.columns.tolist()) # prints all columns in a list

print("\n=== Shape ===")
print(df.shape) #output number of rows and columns

print("\n=== Essay Sets ===")
print(df["essay_set"].value_counts().sort_index())

print("\n=== Score Ranges By Essay Set ===")
print(
    df.groupby("essay_set")["domain1_score"]
      .agg(["min", "max", "mean", "count"])
)

# The dataset contained eight different prompts with different grading scales. 
# To avoid introducing variability caused by differing prompts and rubrics, I restricted the
# analysis to a single essay set. Essay Set 1 was chosen because it contained a large number 
# of essays (1783) and a manageable scoring range of 2–12, making it suitable for reliability analysis.