# AI Grading Reliability Study

## Overview

This project investigates the reliability of large language models (LLMs) for automated essay scoring in educational settings. Using the ASAP Automated Student Assessment Prize (AES) dataset, we compare AI-generated scores against human-assigned resolved scores to evaluate alignment, systematic bias, and practical feasibility for classroom deployment.

**Research Question:** How closely do AI-generated essay grades align with human-assigned grades?

**Secondary Questions:**
- Does AI consistently score essays similarly to humans?
- Which essays produce the largest disagreements?
- What patterns appear in AI grading errors?
- How similar is AI feedback to human feedback?

---

## Dataset

| Property | Value |
|----------|-------|
| **Source** | ASAP AES (Automated Student Assessment Prize) |
| **File** | `training_set_rel3.tsv` |
| **Prompt** | 1 — Argumentative letter to local newspaper |
| **Score Range** | 2–12 (resolved from two human raters, 1–6 each) |
| **Sample Size** | 100 essays (random sample) |
| **Essay Type** | High school argumentative writing |

---

## Methodology

### AI Grading Pipeline
- **Model:** Llama 3.3 70B (via Groq API, free tier)
- **Temperature:** 0.1 (low randomness for consistency)
- **Prompt:** Structured rubric evaluating Organization, Argument Quality, Evidence, Grammar, and Overall Effectiveness
- **Output:** Numeric score (2–12) + short feedback (2–3 sentences)

### Statistical Analysis
- Pearson correlation coefficient
- Mean difference analysis
- Bland-Altman agreement assessment
- Error analysis (top disagreements)

---

## Key Findings

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **N** | 100 essays | Pilot sample |
| **Mean Human Score** | 8.46 | Humans: "average to good" |
| **Mean AI Score** | 5.19 | AI: "below average" |
| **Mean Difference** | **3.27 points** | AI under-grades systematically |
| **Pearson r** | **0.465** | Moderate positive correlation |
| **p-value** | 1.114 × 10⁻⁶ | Statistically significant |

### Interpretation

The AI and human graders show **statistically significant rank-order agreement** (r = 0.465, p &lt; 0.001). Essays rated highly by humans tend to receive relatively higher scores from the AI. However, the AI exhibits a **consistent negative bias of approximately 3.3 points** on the 2–12 scale, suggesting that off-the-shelf LLMs may require calibration or domain-specific fine-tuning before deployment in high-stakes assessment contexts.

### Visualizations

Generated figures saved to `results/figures/`:
- `score_distribution.png` — Human vs. AI score frequency distributions
- `scatter_plot.png` — Score correlation with regression line
- `bland_altman.png` — Clinical agreement analysis

---

## Repository Structure
ai-grading-reliability-study/
├── data/
│   ├── raw/
│   └── processed/
│       └── essays.csv
├── scripts/
│   ├── explore_dataset.py
│   ├── clean_data.py
│   ├── run_ai_grading.py
│   └── analyze_results.py
├── results/
│   ├── figures/
│   │   ├── score_distribution.png
│   │   ├── scatter_plot.png
│   │   └── bland_altman.png
│   └── tables/
│       ├── ai_scores_pilot.csv
│       ├── summary_statistics.csv
│       └── largest_disagreements.csv
├── report/
│   └── (see link below)
├── .env
├── .gitignore
├── requirements.txt
└── README.md


---

## Setup & Reproduction

### Prerequisites
- Python 3.10+
- Free Groq API key ([console.groq.com](https://console.groq.com))

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/ai-grading-reliability-study.git
cd ai-grading-reliability-study

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run pipeline
python scripts/run_ai_grading.py
python scripts/analyze_results.py