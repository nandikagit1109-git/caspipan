def roadmap_prompt(topic):
    return f"""
Create a structured 30-day learning roadmap for {topic}.

Week 1 — Foundations
- Basic concepts
- Beginner practice
- Important terminology

Week 2 — Core Concepts
- Important concepts
- Practical exercises
- Challenges

Week 3 — Practice & Projects
- Intermediate practice
- Real-world applications
- Mini project

Week 4 — Advanced Practice
- Advanced concepts
- Revision
- Final project

For every week include:
- Topics
- Practice tasks
- Mini project
- Learning goal

Keep it realistic for a student and format it clearly.
"""