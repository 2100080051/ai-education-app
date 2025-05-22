import requests
import os
from dotenv import load_dotenv
import streamlit as st


TOGETHER_API_KEY = st.secrets["TOGETHER_API_KEY"]


load_dotenv()

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

    response = requests.post(
        "https://api.together.xyz/v1/completions",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['text'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"
