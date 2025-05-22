import requests
import streamlit as st

TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]

def generate_story(concept, grade, subject):
    prompt = (
        f"Write a fun and simple story that explains the concept '{concept}' "
        f"to a grade {grade} student in {subject}. Make it creative and easy to understand for children."
    )

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = requests.post(
            "https://api.together.xyz/v1/completions",
            headers=headers,
            json=data,
            timeout=15
        )
        response.raise_for_status()  # Raises HTTPError if status != 200
        result = response.json()

        text = result.get('choices', [{}])[0].get('text', '').strip()
        if text:
            return text
        else:
            return "Sorry, no story could be generated at this time."

    except requests.exceptions.RequestException as e:
        # Log the error if needed, here just returning friendly message
        return f"Error contacting API: {e}"

    except Exception as e:
        return f"Unexpected error: {e}"
