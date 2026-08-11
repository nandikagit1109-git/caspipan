import os
import requests
from pathlib import Path
from dotenv import load_dotenv

from .database import get_history


# ==========================================================
# ENVIRONMENT
# ==========================================================

load_dotenv(
    Path(__file__).resolve().parent.parent / ".env"
)


# ==========================================================
# FEATHERLESS
# ==========================================================

API_KEY = os.getenv("FEATHERLESS_API_KEY")

MODEL = os.getenv(
    "FEATHERLESS_MODEL",
    "Qwen/Qwen3-8B"
)


# ==========================================================
# AI PERSONALITY
# ==========================================================

SYSTEM_PROMPT = """
You are Quantum Odyssey, a smart and friendly learning companion.

Your job is to help students learn, understand difficult concepts,
practice skills, and build projects.

You can help with:

• Python
• C
• C++
• Java
• Data Structures and Algorithms
• Artificial Intelligence
• Machine Learning
• Quantum Computing
• Mathematics
• Programming projects
• Study planning
• Career preparation

PERSONALITY:

- Friendly
- Natural
- Clear
- Concise
- Curious
- Patient
- Slightly playful when appropriate

IMPORTANT:

1. Talk like a helpful human tutor, not a customer-service bot.
2. Keep simple questions simple.
3. Explain difficult concepts step by step.
4. Use simple language whenever possible.
5. Give examples when they actually help.
6. When giving code, keep it clean and easy to understand.
7. Use previous conversation context when answering follow-up questions.
8. Adapt explanations to the student's level and previous performance.
9. Ask a short follow-up question when it genuinely helps.
10. Use short bullet points when useful.
11. Keep most answers under 150 words unless the student asks for more detail.
12. Do not give unnecessary motivational speeches.
13. Do not repeatedly introduce yourself.
14. Do not say "I'm your friendly AI learning mentor."
15. Do not use corporate or robotic phrases.
16. Do not repeat the user's question unnecessarily.
17. Do not overuse emojis.
18. Never show internal reasoning, chain-of-thought, or thinking tags to the user.
19. Never output <think>...</think>.
20. Return only the final answer.

NATURAL RESPONSES:

For greetings:
"Hey! 👋 What are you working on today?"

For thanks:
"Anytime!"

For simple confirmations:
"Yep, that's right."
"Cool 👍"
"Got it."

For learning:
"Good question."
"Let's break it down."
"Try this example."

For difficult concepts:
Explain clearly first, then give a small example.
Only give a practice question when it is genuinely useful.
Never output your internal reasoning.
Never output <think> or </think> tags.
Do not describe your reasoning process.
Only return the final response intended for the student.
"""


# ==========================================================
# AI RESPONSE
# ==========================================================

def get_ai_response(user, prompt):

    if not API_KEY:
        return "❌ FEATHERLESS_API_KEY is missing from your .env file."

    history = get_history(
        user,
        limit=10
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": prompt
    })

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1200
    }

    try:

        response = requests.post(
            "https://api.featherless.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

        print("AI STATUS:", response.status_code)

        result = response.json()

        print("AI RESPONSE:", result)

        # ==============================================
        # SUCCESS
        # ==============================================

        if "choices" in result:

            answer = result["choices"][0]["message"]["content"]

            # Remove model reasoning
            if "<think>" in answer:

                if "</think>" in answer:
                    answer = answer.split(
                        "</think>",
                        1
                    )[1].strip()

                else:
                    answer = answer.split(
                        "<think>",
                        1
                    )[0].strip()

            # Remove accidental thinking tags
            answer = answer.replace(
                "<think>",
                ""
            )

            answer = answer.replace(
                "</think>",
                ""
            )

            return answer.strip()


        # ==============================================
        # API ERROR
        # ==============================================

        if "error" in result:

            error = result["error"]

            if isinstance(error, dict):

                return (
                    f"❌ AI Error: "
                    f"{error.get('message', 'Unknown error')}"
                )

            return f"❌ AI Error: {error}"


        return "❌ The AI returned an unexpected response."


    except requests.exceptions.Timeout:

        return "❌ The AI request timed out. Please try again."


    except requests.exceptions.RequestException as e:

        return f"❌ Network error: {e}"


    except Exception as e:

        return f"❌ Unexpected error: {e}"