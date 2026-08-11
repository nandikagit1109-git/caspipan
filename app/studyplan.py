def study_plan_prompt(topic, days):
    return f"""
Create a personalized {days}-day study plan for learning {topic}.

For every phase include:

• Topics to learn
• Daily goals
• Practice exercises
• Revision
• Mini project

Keep the workload realistic for a student.

At the end include:

🎯 Final Goal
📌 Recommended Daily Study Time
🏆 Final Project
"""


def study_plan_intro(topic, days):
    return f"""
📚 QUANTUM STUDY PLAN

Topic: {topic}
Duration: {days} days

Let's build your learning journey! 🚀
"""