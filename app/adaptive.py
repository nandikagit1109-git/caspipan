def adaptive_prompt(topic, score=None):
    if score is None:
        return f"""
Create one short learning challenge about {topic}.

Rules:
- Make it suitable for a beginner/intermediate student.
- Give only ONE challenge.
- Keep it under 100 words.
- Do not give the answer.
- Ask the student to reply with their solution.
"""

    if score < 60:
        difficulty = "beginner"
        instruction = "Focus on rebuilding the student's understanding."
    else:
        difficulty = "intermediate"
        instruction = "Make the challenge slightly harder."

    return f"""
Create ONE {difficulty} learning challenge about {topic}.

The student scored {score}% previously.

{instruction}

Rules:
- Keep it under 100 words.
- Do not give the answer.
- Ask the student to reply with their solution.
"""
