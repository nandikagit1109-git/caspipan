import random


MISSIONS = [
    "📘 Learn one new Python concept.",
    "💻 Solve two programming problems.",
    "🤖 Learn one Artificial Intelligence concept.",
    "🧠 Revise something you learned yesterday.",
    "⚛️ Learn one Quantum Computing concept.",
    "📚 Study for 30 focused minutes.",
    "🚀 Build a tiny programming project.",
    "🔍 Read about one new technology."
]


def get_mission():
    mission = random.choice(MISSIONS)

    return f"""
🎯 TODAY'S MISSION

{mission}

━━━━━━━━━━━━━━━━━━

⭐ Reward: +50 XP

Complete it and keep your learning streak alive! 🔥
"""