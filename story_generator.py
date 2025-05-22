import requests
import streamlit as st
import requests

TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]


def generate_story_full_prompt(prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
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
        response.raise_for_status()
        result = response.json()
        text = result.get('choices', [{}])[0].get('text', '').strip()
        if text:
            return text
        else:
            return "Sorry, no story could be generated at this time."

    except requests.exceptions.RequestException as e:
        return f"Error contacting API: {e}"

    except Exception as e:
        return f"Unexpected error: {e}"
