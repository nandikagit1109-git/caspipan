import os
import requests

API_KEY = os.getenv("FEATHERLESS_API_KEY")

# CHANGE THIS LATER IF NEEDED
MODEL = "meta-llama/Llama-3.1-8B-Instruct"


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
                "content":
                """
You are Quantum Odyssey.

You are an AI mentor.

You teach:
Python
C++
Java
AI
Machine Learning
Quantum Computing
DSA

Always explain in simple language.

Keep answers concise but useful.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    try:

        response = requests.post(
            "https://api.featherless.ai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        return f"Error:\n{e}"