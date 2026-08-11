def build_weakness_alert(topic, score):
    if score < 60:
        return (
            f"🚨 Quantum Odyssey Alert\n\n"
            f"You may need more practice with {topic}.\n"
            f"Current average: {score}%\n\n"
            f"🎯 Try one short challenge today."
        )

    if score < 80:
        return (
            f"📚 Quantum Odyssey Update\n\n"
            f"You're improving in {topic}.\n"
            f"Current average: {score}%\n\n"
            f"🎯 Keep practicing!"
        )

    return (
        f"🚀 Quantum Odyssey Update\n\n"
        f"You're doing well in {topic}!\n"
        f"Current average: {score}%\n\n"
        f"🎯 Ready for a harder challenge?"
    )