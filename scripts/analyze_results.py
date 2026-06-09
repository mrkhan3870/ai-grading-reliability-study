"""
analyze_results.py
Compare human and AI scores, calculate correlation, generate visualizations.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Paths
RESULTS_DIR = "results"
FIGURES_DIR = os.path.join(RESULTS_DIR, "figures")
TABLES_DIR = os.path.join(RESULTS_DIR, "tables")

os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# Load data
df = pd.read_csv(
    os.path.join(TABLES_DIR, "benchmark_results.csv")
)
models = [
    "groq",
    "gemini",
    "cerebras"
]

# Convert to numeric
df["human_score"] = pd.to_numeric(df["human_score"])
df["ai_score"] = pd.to_numeric(df["ai_score"])

# ----------------------------------------
# Summary Statistics
# ----------------------------------------

summary_rows = []

for model in models:

    temp = df.dropna(
        subset=[
            "human_score",
            f"{model}_score"
        ]
    )

    r, p = stats.pearsonr(
        temp["human_score"],
        temp[f"{model}_score"]
    )

    mae = np.mean(
        np.abs(
            temp["human_score"]
            - temp[f"{model}_score"]
        )
    )

    rmse = np.sqrt(
        np.mean(
            (
                temp["human_score"]
                - temp[f"{model}_score"]
            ) ** 2
        )
    )

    summary_rows.append({
        "Model": model,
        "N": len(temp),
        "Mean Human": round(
            temp["human_score"].mean(),
            2
        ),
        "Mean AI": round(
            temp[f"{model}_score"].mean(),
            2
        ),
        "Pearson r": round(r, 3),
        "MAE": round(mae, 3),
        "RMSE": round(rmse, 3)
    })

summary = pd.DataFrame(summary_rows)

summary.to_csv(
    os.path.join(
        TABLES_DIR,
        "summary_statistics.csv"
    ),
    index=False
)

print(summary)
print("Summary Statistics:")
print(summary.to_string(index=False))
print()

# ----------------------------------------
# Score Distribution Comparison
# ----------------------------------------
agreement_rows = []

pairs = [
    ("groq", "gemini"),
    ("groq", "cerebras"),
    ("gemini", "cerebras")
]

for m1, m2 in pairs:

    temp = df.dropna(
        subset=[
            f"{m1}_score",
            f"{m2}_score"
        ]
    )

    r, _ = stats.pearsonr(
        temp[f"{m1}_score"],
        temp[f"{m2}_score"]
    )

    agreement_rows.append({
        "Model_1": m1,
        "Model_2": m2,
        "Correlation": round(r, 3)
    })
    

agreement_df = pd.DataFrame(
    agreement_rows
)

agreement_df.to_csv(
    os.path.join(
        TABLES_DIR,
        "inter_agent_agreement.csv"
    ),
    index=False
)

# Score Distribution Comparison

plt.figure(figsize=(10, 6))

bins = np.arange(1.5, 13.5, 1)

plt.hist(
    df["human_score"],
    bins=bins,
    alpha=0.5,
    label="Human"
)

for model in models:

    plt.hist(
        df[f"{model}_score"],
        bins=bins,
        alpha=0.3,
        label=model.capitalize()
    )

plt.legend()

plt.xlabel("Score")
plt.ylabel("Frequency")

plt.title(
    "Score Distribution Comparison"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        FIGURES_DIR,
        "score_distribution.png"
    ),
    dpi=300
)

plt.close()

# ----------------------------------------
# Scatter Plot with Regression Line
# ----------------------------------------

for model in models:

    temp = df.dropna(
        subset=[
            "human_score",
            f"{model}_score"
        ]
    )

    r, _ = stats.pearsonr(
        temp["human_score"],
        temp[f"{model}_score"]
    )

    plt.figure(figsize=(8, 8))

    plt.scatter(
        temp["human_score"],
        temp[f"{model}_score"],
        alpha=0.6
    )

    plt.plot(
        [2, 12],
        [2, 12],
        "k:"
    )

    plt.xlabel(
        "Human Score"
    )

    plt.ylabel(
        f"{model.capitalize()} Score"
    )

    plt.title(
        f"Human vs {model.capitalize()} (r={r:.3f})"
    )

    plt.savefig(
        os.path.join(
            FIGURES_DIR,
            f"{model}_scatter.png"
        ),
        dpi=300
    )

    plt.close()


# ----------------------------------------
# Error Analysis: Largest Disagreements
# ----------------------------------------

all_errors = []
for model in models:

    temp = df.copy()

    temp["abs_diff"] = (
        temp["human_score"]
        - temp[f"{model}_score"]
    ).abs()

    largest = temp.nlargest(
        10,
        "abs_diff"
    )

    largest["model"] = model

    all_errors.append(
        largest[
            [
                "essay_id",
                "human_score",
                f"{model}_score",
                "abs_diff",
                "model"
            ]
        ]
    )
    
largest_errors = pd.concat(
    all_errors
)

largest_errors.to_csv(
    os.path.join(
        TABLES_DIR,
        "largest_disagreements.csv"
    ),
    index=False
)

# Correlation Heatmap
corr_matrix = df[
    [
        "human_score",
        "groq_score",
        "gemini_score",
        "cerebras_score"
    ]
].corr()

plt.figure(figsize=(8, 6))

plt.imshow(
    corr_matrix,
    interpolation="nearest"
)

plt.colorbar()

plt.xticks(
    range(len(corr_matrix.columns)),
    corr_matrix.columns,
    rotation=45
)

plt.yticks(
    range(len(corr_matrix.columns)),
    corr_matrix.columns
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        FIGURES_DIR,
        "correlation_heatmap.png"
    ),
    dpi=300
)

plt.close()