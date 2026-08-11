def quiz_prompt(topic):
    return f"""
Create a fun educational quiz about {topic}.

Create exactly 5 multiple-choice questions.

For each question provide:

Question:
A)
B)
C)
D)

Correct Answer:
Explanation:

Make the questions suitable for a student.

Do not make all correct answers the same option.
"""


def quiz_intro(topic):
    return f"""
🧠 QUANTUM QUIZ

Topic: {topic}

Let's test your knowledge! 🚀
"""