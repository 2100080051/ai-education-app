# story_generator.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Configure Groq (OpenAI‐compatible) endpoint
openai.api_base = "https://api.groq.com/openai/v1"
openai.api_key = os.getenv("GROQ_API_KEY")


def generate_science_story(topic: str, grade: int) -> str:
    prompt = (
        f"Write a fun, cartoon-style science story about '{topic}' for a grade {grade} student. "
        "Make it engaging, clear, and suitable for children."
    )
    response = openai.ChatCompletion.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )
    return response.choices[0].message.content.strip()


def generate_science_explanation(topic: str, grade: int) -> str:
    prompt = (
        f"Explain the science concept '{topic}' in simple words for a grade {grade} student. "
        "Use short, clear sentences and define any new words."
    )
    response = openai.ChatCompletion.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()


def generate_math_story(topic: str, grade: int) -> str:
    prompt = (
        f"Write a short, playful story about a character learning '{topic}' "
        f"for a grade {grade} student. Include a simple worked example (e.g., 3 × 4 = 12) "
        "and make it engaging and kid-friendly."
    )
    response = openai.ChatCompletion.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )
    return response.choices[0].message.content.strip()


def generate_math_explanation(topic: str, grade: int) -> str:
    prompt = (
        f"Explain the math concept '{topic}' step by step for a grade {grade} student. "
        "Include a few simple practice problems and their answers in the explanation."
    )
    response = openai.ChatCompletion.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()


def generate_history_story(topic: str, grade: int) -> str:
    prompt = (
        f"Write an engaging narrative story about the historical/geographical topic '{topic}' "
        f"for a grade {grade} student. Include key events, characters, or locations, and keep it easy to follow."
    )
    response = openai.ChatCompletion.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )
    return response.choices[0].message.content.strip()


def generate_history_explanation(topic: str, grade: int) -> str:
    prompt = (
        f"Explain the significance of '{topic}' (history or geography) in simple terms for a grade {grade} student. "
        "Include important dates, places or facts, and why it matters today."
    )
    response = openai.ChatCompletion.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()
