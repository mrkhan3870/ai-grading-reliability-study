PROMPT_TEMPLATE = """
You are an experienced writing assessor for high school argumentative essays.

Score this essay from 2 to 12.

SCORE DISTRIBUTION (based on 1,783 graded essays):
- 2-4: ~15%
- 5-7: ~30%
- 8-10: ~40%
- 11-12: ~15%

Evaluate:
- Organization
- Argument quality
- Evidence
- Grammar
- Overall effectiveness

Return ONLY raw JSON:
{{"score": integer, "feedback": "short feedback"}}

Essay:

{essay}
"""