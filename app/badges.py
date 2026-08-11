def get_badge(xp):

    if xp >= 2000:
        return "👑 Quantum Master"

    if xp >= 1200:
        return "🏆 AI Expert"

    if xp >= 800:
        return "🥇 Advanced Learner"

    if xp >= 500:
        return "🥈 Knowledge Explorer"

    if xp >= 250:
        return "🥉 Rising Learner"

    if xp >= 100:
        return "🌱 Beginner"

    return "✨ New Learner"