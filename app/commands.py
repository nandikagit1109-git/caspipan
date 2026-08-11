from .xp import get_xp, get_level
from .badges import get_badge
from .missions import get_mission
from .streak import get_streak
from .leaderboard import format_leaderboard
from .quiz import quiz_prompt
from .roadmap import roadmap_prompt
from .studyplan import study_plan_prompt
from .adaptive import adaptive_prompt
from .database import save_performance,get_average_score
from .notification import build_weakness_alert


def get_help():

    return """
🌌 QUANTUM ODYSSEY

Available Commands

/help
Show all commands.

/xp
Check XP, level and badge.

/mission
Get today's learning mission.

/quiz [topic]
Generate a 5-question quiz.

/roadmap [topic]
Generate a 30-day learning roadmap.

/studyplan [topic] [days]
Create a personalized study plan.

/leaderboard
See the top learners.

You can also simply ask me anything! 🧠
"""


def handle_command(user, text):

    lower = text.lower().strip()

    # HELP
    if lower == "/help":
        return {
            "type": "reply",
            "text": get_help()
        }

    # XP
    if lower == "/xp":

        xp = get_xp(user)
        level = get_level(xp)
        badge = get_badge(xp)
        streak = get_streak(user)
        

        return {
            "type": "reply",
            "text": f"""
⭐ YOUR QUANTUM PROGRESS

XP: {xp}

🏆 Level: {level}

🎖 Badge: {badge}

🔥 Streak: {streak} day(s)
"""
        }

    # MISSION
    if lower == "/mission":

        return {
            "type": "reply",
            "text": get_mission()
        }

    # LEADERBOARD
    if lower == "/leaderboard":

        return {
            "type": "reply",
            "text": format_leaderboard()
        }

    # QUIZ
    if lower.startswith("/quiz"):

        topic = text[5:].strip()

        if not topic:
            topic = "Python"

        return {
            "type": "ai",
            "prompt": quiz_prompt(topic),
            "prefix": f"🧠 QUIZ: {topic}\n\n"
        }

    # ROADMAP
    if lower.startswith("/roadmap"):

        topic = text[8:].strip()

        if not topic:
            topic = "Python"

        return {
            "type": "ai",
            "prompt": roadmap_prompt(topic),
            "prefix": f"🗺️ ROADMAP: {topic}\n\n"
        }

    # STUDY PLAN
    if lower.startswith("/studyplan"):

        parts = text.split()

        if len(parts) < 3:

            return {
                "type": "reply",
                "text": """
❌ Usage:

/studyplan <topic> <days>

Example:

/studyplan Python 30
"""
            }

        topic = parts[1]

        try:
            days = int(parts[2])
        except ValueError:
            days = 30

        if days < 1:
            days = 1

        if days > 365:
            days = 365

        return {
            "type": "ai",
            "prompt": study_plan_prompt(topic, days),
            "prefix": f"📚 {days}-DAY STUDY PLAN: {topic}\n\n"
        }
        if lower == "/progress":

           xp = get_xp(user)
           level = get_level(xp)
           badge = get_badge(xp)
           streak = get_streak(user)

        return {
            "type": "reply",
            "text": f"""📊 YOUR PROGRESS

            ⭐ XP: {xp}
            🏆 Level: {level}
            🎖 Badge: {badge}
            🔥 Streak: {streak} day(s)
            """
    }
        if lower.startswith("/challenge"):
 
         topic = text[len("/challenge"):].strip()

        if not topic:
          topic = "Python"

        return {
        "type": "ai",
        "prompt": adaptive_prompt(topic),
        "prefix": "🎯 ADAPTIVE CHALLENGE\n\n"
    }
        if lower.startswith("/evaluate"):

          answer = text[len("/evaluate"):].strip()

        if not answer:
            return {
                "type": "reply",
                "text": "Please provide your answer after /evaluate."
            }

        prompt = evaluation_prompt(
            "Python loops",
            "Write a Python loop that prints numbers from 1 to 5.",
            answer
        )

        return {
            "type": "ai",
            "prompt": prompt,
            "prefix": "🧠 EVALUATION\n\n"
        }
            # ==================================================
    # WEAKNESS
    # ==================================================

        if lower == "/weakness":

          return {
            "type": "ai",
            "prompt": """
Based on the student's learning history, identify ONE topic
they should practice more.

Keep the response very short.

Format:

🧠 Weak Area: <topic>
🎯 Why: <one short sentence>
💡 Next Step: <one short practice suggestion>
""",
            "prefix": ""
        }
        if lower.startswith("/savescore"):

           parts = text.split()

        if len(parts) < 3:
            return {
                "type": "reply",
                "text": "Use: /savescore Python 80"
            }

        topic = parts[1]

        try:
            score = int(parts[2])
        except ValueError:
            return {
                "type": "reply",
                "text": "Score must be a number."
            }

        save_performance(user, topic, score)

        return {
            "type": "reply",
            "text": f"✅ Saved {topic} score: {score}%"
        }
            # ==================================================
    # NEXT ADAPTIVE CHALLENGE
    # ==================================================

        if lower.startswith("/next"):

         topic = text[len("/next"):].strip()

        if not topic:
            topic = "Python"

        score = get_average_score(user, topic)

        if score is None:
            score = 50

        prompt = adaptive_prompt(topic, score)

        return {
            "type": "ai",
            "prompt": prompt,
            "prefix": "🎯 NEXT CHALLENGE\n\n"
        }
            # ==================================================
    # NOTIFICATION TEST
    # ==================================================

        if lower.startswith("/notify"):

          text_to_send = text[len("/notify"):].strip()

        if not text_to_send:
            text_to_send = "You have a new learning challenge! 🎯"

        return {
            "type": "reply",
            "text": f"🔔 Quantum Odyssey\n\n{text_to_send}"
        }
              # ==================================================
    # SMART REMINDER
    # ==================================================

        if lower.startswith("/remind"):

          topic = text[len("/remind"):].strip()

        if not topic:
            topic = "Python"

        score = get_average_score(user, topic)

        if score is None:
            reminder = (
                f"🎯 You haven't practiced {topic} yet. "
                f"Try a challenge today!"
            )

        elif score < 60:
            reminder = (
                f"🧠 You should practice {topic} today. "
                f"Your current average is {score}%."
            )

        else:
            reminder = (
                f"🚀 You're doing well in {topic} "
                f"with an average of {score}%. "
                f"Try a harder challenge!"
            )

        return {
            "type": "reply",
            "text": reminder
        }

             # ==================================================
    # PERSONAL COACH
    # ==================================================

        if lower.startswith("/coach"):

         topic = text[len("/coach"):].strip()

        if not topic:
            topic = "Python"

        score = get_average_score(user, topic)

        if score is None:
            score = 0

        prompt = f"""
You are Quantum Odyssey, a short-form learning coach.

Student topic: {topic}
Student average score: {score}%

Give the student ONE very short personalized coaching message.

Rules:
- Maximum 60 words.
- Be encouraging but not overly dramatic.
- Give exactly ONE actionable next step.
"""

        return {
            "type": "ai",
            "prompt": prompt,
            "prefix": "🧠 COACH\n\n"
        }
            # ==================================================
    # TODAY'S ACTION
    # ==================================================

        if lower.startswith("/today"):

         topic = text[len("/today"):].strip()

        if not topic:
            topic = "Python"

        score = get_average_score(user, topic)

        if score is None:
            score = 0

        if score < 60:
            action = f"Practice one beginner {topic} challenge."
        elif score < 80:
            action = f"Practice one intermediate {topic} challenge."
        else:
            action = f"Try one advanced {topic} challenge."

        return {
            "type": "reply",
            "text": f"🎯 TODAY\n\n{action}"
        }
               # ==================================================
    # LEARNER PROFILE
    # ==================================================

        if lower == "/profile":

         xp = get_xp(user)
        level = get_level(xp)
        badge = get_badge(xp)

        return {
            "type": "reply",
            "text": f"""🌌 QUANTUM PROFILE

⭐ XP: {xp}
🏆 Level: {level}
🎖 Badge: {badge}
"""
        }
            # ==================================================
    # SMART LEARNING ALERT
    # ==================================================

        if lower.startswith("/alert"):

          topic = text[len("/alert"):].strip()

        if not topic:
            topic = "Python"

        score = get_average_score(user, topic)

        if score is None:
            return {
                "type": "reply",
                "text": f"📚 No performance data for {topic} yet."
            }

        alert = build_weakness_alert(topic, score)

        return {
            "type": "reply",
            "text": alert
        }
    return None