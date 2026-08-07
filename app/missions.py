import random

MISSIONS = [

    "📘 Learn Python loops today.",

    "💻 Solve 2 DSA questions.",

    "🤖 Read one AI article.",

    "⚛ Learn one Quantum Computing concept.",

    "📚 Practice Python for 30 minutes.",

    "🧠 Revise Object-Oriented Programming."

]

def get_mission():

    return f"""🎯 Today's Mission

{random.choice(MISSIONS)}

Reward
⭐ +50 XP
🏆 Mission Badge
"""