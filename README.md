# AI Grading Reliability Study

## Overview

This project investigates the reliability of large language models (LLMs) for automated essay scoring in educational settings. Using the ASAP Automated Student Assessment Prize (AES) dataset, the study compares scores assigned by multiple AI models against human-assigned grades and examines agreement both between humans and AI systems and among the AI systems themselves.

The project was designed as a reproducible benchmarking framework, allowing multiple grading models to be evaluated using the same dataset, rubric, prompt, and analysis pipeline.

**Primary Research Question:**
How closely do AI-generated essay grades align with human-assigned grades?

**Secondary Research Questions:**

* Which AI model most closely matches human evaluation?
* How much agreement exists between different AI grading systems?
* Which essays produce the largest disagreements?
* What patterns appear in AI grading errors?
* Can multiple AI systems provide consistent educational assessment?

---

## Models Evaluated

| Model                   | Provider      |
| ----------------------- | ------------- |
| Llama 3.3 70B Versatile | Groq          |
| Gemini 2.5 Flash        | Google Gemini |
| Llama-based Model       | Cerebras      |

All models receive identical grading instructions and evaluate the same essays independently.

---

## Dataset

| Property     | Value                                            |
| ------------ | ------------------------------------------------ |
| Source       | ASAP Automated Student Assessment Prize (AES)    |
| File         | `training_set_rel3.tsv`                          |
| Prompt       | 1 — Argumentative Letter to a Local Newspaper    |
| Score Range  | 2–12                                             |
| Human Scores | Resolved score from two independent human raters |
| Sample Size  | 100 essays (random sample)                       |
| Essay Type   | High-school argumentative writing                |

---

## Methodology

### Data Preparation

1. Load ASAP AES dataset
2. Filter Prompt 1 essays
3. Clean and preprocess submissions
4. Randomly sample 100 essays for evaluation

### Grading Pipeline

Each essay is evaluated independently by:

* Groq Agent
* Gemini Agent
* Cerebras Agent

All models receive:

* Identical prompt
* Identical rubric
* Identical scoring range (2–12)

Evaluation criteria:

* Organization
* Argument Quality
* Evidence
* Grammar
* Overall Effectiveness

Each model returns:

```json
{
  "score": 8,
  "feedback": "Well-organized argument with relevant evidence."
}
```

### Analysis

Human-AI comparisons:

* Pearson Correlation
* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)

Inter-model comparisons:

* Groq vs Gemini
* Groq vs Cerebras
* Gemini vs Cerebras

Additional analyses:

* Largest disagreement cases
* Score distribution comparison
* Correlation heatmap
* Scatter plot visualization

---

## Repository Structure

```text
ai-grading-reliability-study/

├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── groq_agent.py
│   │   ├── gemini_agent.py
│   │   └── cerebras_agent.py
│   │
│   ├── run_ai_grading.py
│   ├── run_benchmark.py
│   └── analyze_results.py
│
├── results/
│   ├── tables/
│   └── figures/
│
├── report/
│   └── grading_rubric.md
│
└── README.md
```

---

## Outputs

### Tables

Generated in:

```text
results/tables/
```

Files:

* `benchmark_results.csv`
* `summary_statistics.csv`
* `largest_disagreements.csv`
* `inter_agent_agreement.csv`

### Figures

Generated in:

```text
results/figures/
```

Files:

* `score_distribution.png`
* `groq_scatter.png`
* `gemini_scatter.png`
* `cerebras_scatter.png`
* `correlation_heatmap.png`

---

## Reproducing the Study

### Prerequisites

* Python 3.10+
* Groq API Key
* Gemini API Key
* Cerebras API Key

### Installation

```bash
git clone https://github.com/yourusername/ai-grading-reliability-study.git

cd ai-grading-reliability-study

python -m venv .venv

source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_key

GEMINI_API_KEY=your_gemini_key

CEREBRAS_API_KEY=your_cerebras_key
```

### Run Benchmark

```bash
python scripts/run_benchmark.py
```

### Generate Analysis

```bash
python scripts/analyze_results.py
```

---

## Future Work

Potential extensions include:

* Larger evaluation samples
* Additional foundation models
* Rubric-specific scoring dimensions
* Ensemble grading approaches
* Qualitative feedback comparison
* Statistical agreement metrics such as Cohen's Kappa
* Multimodal grading of PDFs and handwritten submissions

---

## Research Motivation

Educational institutions are increasingly exploring AI-assisted assessment systems. Before such systems can be deployed responsibly, their reliability must be measured against human evaluators and against competing AI systems.

This project provides a reproducible framework for studying grading consistency, agreement, and bias across multiple state-of-the-art language models.
