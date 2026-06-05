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
df = pd.read_csv(os.path.join(TABLES_DIR, "ai_scores_pilot.csv"))

# Drop any failed rows
df = df.dropna(subset=["ai_score", "human_score"])

# Convert to numeric
df["human_score"] = pd.to_numeric(df["human_score"])
df["ai_score"] = pd.to_numeric(df["ai_score"])

# ----------------------------------------
# Summary Statistics
# ----------------------------------------

n = len(df)
mean_human = df["human_score"].mean()
mean_ai = df["ai_score"].mean()
std_human = df["human_score"].std()
std_ai = df["ai_score"].std()

# Pearson correlation
r, p_value = stats.pearsonr(df["human_score"], df["ai_score"])

# Mean difference (human - AI)
mean_diff = (df["human_score"] - df["ai_score"]).mean()
std_diff = (df["human_score"] - df["ai_score"]).std()

# ----------------------------------------
# Save Summary Table
# ----------------------------------------

summary = pd.DataFrame({
    "Metric": [
        "N (essays)",
        "Mean Human Score",
        "Mean AI Score",
        "Std Human Score",
        "Std AI Score",
        "Pearson r",
        "p-value",
        "Mean Difference (Human - AI)",
        "Std Difference"
    ],
    "Value": [
        n,
        round(mean_human, 2),
        round(mean_ai, 2),
        round(std_human, 2),
        round(std_ai, 2),
        round(r, 3),
        f"{p_value:.3e}" if p_value < 0.001 else round(p_value, 3),
        round(mean_diff, 2),
        round(std_diff, 2)
    ]
})

summary.to_csv(os.path.join(TABLES_DIR, "summary_statistics.csv"), index=False)
print("Summary Statistics:")
print(summary.to_string(index=False))
print()

# ----------------------------------------
# Score Distribution Comparison
# ----------------------------------------

plt.figure(figsize=(10, 6))
bins = np.arange(1.5, 13.5, 1)

plt.hist(df["human_score"], bins=bins, alpha=0.6, label="Human", color="steelblue", edgecolor="black")
plt.hist(df["ai_score"], bins=bins, alpha=0.6, label="AI", color="coral", edgecolor="black")

plt.xlabel("Score")
plt.ylabel("Frequency")
plt.title("Score Distribution: Human vs AI")
plt.legend()
plt.xticks(range(2, 13))
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "score_distribution.png"), dpi=300)
plt.close()
print("Saved: score_distribution.png")

# ----------------------------------------
# Scatter Plot with Regression Line
# ----------------------------------------

plt.figure(figsize=(8, 8))

plt.scatter(df["human_score"], df["ai_score"], alpha=0.6, color="steelblue", edgecolors="black", s=60)

# Regression line
z = np.polyfit(df["human_score"], df["ai_score"], 1)
p = np.poly1d(z)
plt.plot(df["human_score"], p(df["human_score"]), "r--", alpha=0.8, label=f"r = {r:.3f}")

# Perfect agreement line
plt.plot([2, 12], [2, 12], "k:", alpha=0.5, label="Perfect Agreement")

plt.xlabel("Human Score")
plt.ylabel("AI Score")
plt.title("Human vs AI Scores")
plt.xlim(1, 13)
plt.ylim(1, 13)
plt.xticks(range(2, 13))
plt.yticks(range(2, 13))
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "scatter_plot.png"), dpi=300)
plt.close()
print("Saved: scatter_plot.png")

# ----------------------------------------
# Bland-Altman Plot
# ----------------------------------------

diff = df["human_score"] - df["ai_score"]
mean = (df["human_score"] + df["ai_score"]) / 2

plt.figure(figsize=(10, 6))

plt.scatter(mean, diff, alpha=0.6, color="steelblue", edgecolors="black", s=60)

# Mean difference line
plt.axhline(y=mean_diff, color="red", linestyle="--", label=f"Mean diff = {mean_diff:.2f}")

# 95% limits of agreement
loa_lower = mean_diff - 1.96 * std_diff
loa_upper = mean_diff + 1.96 * std_diff
plt.axhline(y=loa_lower, color="gray", linestyle=":", label=f"95% LoA: {loa_lower:.1f} to {loa_upper:.1f}")
plt.axhline(y=loa_upper, color="gray", linestyle=":")

plt.xlabel("Mean Score (Human + AI) / 2")
plt.ylabel("Difference (Human - AI)")
plt.title("Bland-Altman Plot: Human vs AI Agreement")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "bland_altman.png"), dpi=300)
plt.close()
print("Saved: bland_altman.png")

# ----------------------------------------
# Error Analysis: Largest Disagreements
# ----------------------------------------

df["abs_diff"] = (df["human_score"] - df["ai_score"]).abs()
largest_errors = df.nlargest(10, "abs_diff")[["essay_id", "human_score", "ai_score", "abs_diff"]]

largest_errors.to_csv(os.path.join(TABLES_DIR, "largest_disagreements.csv"), index=False)
print("\nTop 10 Largest Disagreements:")
print(largest_errors.to_string(index=False))

print("\n" + "="*50)
print("Analysis complete. Outputs saved to results/")
print("="*50)