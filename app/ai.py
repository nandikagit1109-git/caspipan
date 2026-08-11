import os
import requests
from pathlib import Path
from dotenv import load_dotenv

from .database import get_history


load_dotenv(
    Path(__file__).resolve().parent.parent / ".env"
)


API_KEY = os.getenv("FEATHERLESS_API_KEY")

MODEL = os.getenv(
    "FEATHERLESS_MODEL",
    "Qwen/Qwen3-8B"
)


SYSTEM_PROMPT = """
You are Quantum Odyssey, a friendly AI learning mentor.

Your job is to help students learn and understand difficult concepts.

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

Rules:

1. Explain concepts clearly and step by step.
2. Use simple language when possible.
3. Give examples.
4. When giving code, make it clean and easy to understand.
5. Encourage learning without being overly verbose.
6. If the student asks a follow-up question, use previous conversation context.
7. End educational explanations with a small practice question when appropriate.
8.Keep answers concise.
9.Avoid unnecessary introductions.
10.Do not add motivational paragraphs.
11.Use short bullet points when helpful.
12.Keep most answers under 150 words unless the user asks for more detail.
"""


def get_ai_response(user, prompt):

    if not API_KEY:
        return "❌ FEATHERLESS_API_KEY is missing from your .env file."

    history = get_history(user, limit=10)

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

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        if "error" in result:
            error = result["error"]

            if isinstance(error, dict):
                return f"❌ AI Error: {error.get('message', 'Unknown error')}"

            return f"❌ AI Error: {error}"

        return "❌ The AI returned an unexpected response."

    except requests.exceptions.Timeout:
        return "❌ The AI request timed out. Please try again."

    except requests.exceptions.RequestException as e:
        return f"❌ Network error: {e}"

    except Exception as e:
        return f"❌ Unexpected error: {e}"