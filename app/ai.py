import os
from unittest import result
from urllib import response
import requests

API_KEY = os.getenv("FEATHERLESS_API_KEY")

# CHANGE THIS LATER IF NEEDED
MODEL = "Qwen/Qwen3-8B"

def get_ai_response(prompt):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": """
You are Quantum Odyssey.

You are a friendly AI mentor for students.

Your job is to help students learn:

• Python
• C++
• Java
• Data Structures & Algorithms
• Artificial Intelligence
• Machine Learning
• Quantum Computing

Rules:

1. Explain concepts step by step.
2. Use simple language.
3. Give examples whenever possible.
4. End every answer with one practice question.
5. Encourage the student to keep learning.
6. Keep answers concise but informative.
"""            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(
            "https://api.featherless.ai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        print("STATUS:", response.status_code)

        result = response.json()

        print("FULL RESPONSE:", result)

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return str(result)

    except Exception as e:
        return f"Error: {e}"