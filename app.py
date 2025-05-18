# app.py

import os
import requests
import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
from streamlit_lottie import st_lottie

from story_generator import (
    generate_science_story, generate_science_explanation,
    generate_math_story, generate_math_explanation,
    generate_history_story, generate_history_explanation
)

# Ensure static/ folder exists for saving audio
if not os.path.isdir("static"):
    os.makedirs("static")


# ---- Helper: load Lottie animation from URL ----
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None
    return None

# Preload Lottie animations
lottie_welcome = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_touohxv0.json")
lottie_rocket  = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_iwmd6pyr.json")
lottie_math    = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_j1adxtia.json")  # Math-themed
lottie_world   = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_pprxh53t.json")   # Globe/Map


# ---- Page Config & CSS ----
st.set_page_config(
    page_title="🌟 Interactive 3-Language Story & Education",
    layout="wide",
    page_icon="🧒"
)

# Custom CSS: particle background + hover effects
st.markdown("""
    <style>
    /* Particle background via canvas */
    body {
        margin: 0;
        padding: 0;
        background: #FFF8E1;
        overflow-x: hidden;
    }
    #particles-js {
        position: fixed;
        width: 100%;
        height: 100%;
        z-index: -1;
        top: 0; left: 0;
    }
    h1, h2, h3 {
        color: #4CAF50;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    .block-container {
        padding: 2rem 4rem;
    }
    .stButton > button {
        background-color: #FF7043;
        color: white;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        transition: transform 0.2s ease-in-out;
    }
    .stButton > button:hover {
        transform: scale(1.05);
    }
    /* Style section headers with emoji */
    h4 {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #FB8C00;
    }
    </style>
""", unsafe_allow_html=True)

# Particle.js script (lightweight star/particle effect)
st.markdown("""
    <div id="particles-js"></div>
    <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
    <script>
      particlesJS("particles-js", {
        "particles": {
          "number": { "value": 50 },
          "color": { "value": "#ffd54f" },
          "shape": { "type": "circle" },
          "opacity": { "value": 0.6 },
          "size": { "value": 3 },
          "move": { "enable": true, "speed": 1 }
        },
        "interactivity": {
          "events": { "onhover": { "enable": true, "mode": "repulse" } }
        }
      });
    </script>
""", unsafe_allow_html=True)


# ---- Header Section with Lottie ----
st.markdown("<h1 style='text-align:center;'>🌟 3-Language Story & Education 🌟</h1>", unsafe_allow_html=True)
if lottie_welcome:
    st_lottie(lottie_welcome, height=200, key="welcome")

st.markdown("<h3 style='text-align:center;'>Choose a subject below, then read/listen in English, తెలుగు, हिन्दी!</h3>", unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html=True)


# ---- Sidebar Inputs ----
with st.sidebar:
    st.header("🔍 Select Subject, Topic & Grade")
    subject = st.selectbox("Subject", ["Science", "Math", "History/Geography"])
    topic = st.text_input(f"Enter a {subject} Topic", "")
    grade = st.selectbox("Select Grade", ["3", "4", "5", "6", "7"])
    if st.button("Generate Everything 🎈"):
        st.session_state.generate_flag = True


# ---- Session State Initialization ----
if "generate_flag" not in st.session_state:
    st.session_state.generate_flag = False

for key in [
    "story_en", "story_te", "story_hi",
    "audio_en", "audio_te", "audio_hi",
    "explanation_en", "explanation_te", "explanation_hi"
]:
    if key not in st.session_state:
        st.session_state[key] = ""

if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False


# ---- On Generate Button Click ----
if st.session_state.generate_flag:
    if not topic.strip():
        st.warning("Please enter a topic.")
        st.session_state.generate_flag = False
    else:
        with st.spinner("🛠️ Generating story, audio, and explanations..."):
            # 1. Generate story & explanation based on subject
            if subject == "Science":
                story_en = generate_science_story(topic, int(grade))
                explanation_en = generate_science_explanation(topic, int(grade))
                animation = lottie_rocket
            elif subject == "Math":
                story_en = generate_math_story(topic, int(grade))
                explanation_en = generate_math_explanation(topic, int(grade))
                animation = lottie_math
            else:  # History/Geography
                story_en = generate_history_story(topic, int(grade))
                explanation_en = generate_history_explanation(topic, int(grade))
                animation = lottie_world

            # Store English story
            st.session_state.story_en = story_en

            # 2. Translate story to Telugu & Hindi
            translator_te = GoogleTranslator(source="en", target="te")
            translator_hi = GoogleTranslator(source="en", target="hi")
            st.session_state.story_te = translator_te.translate(story_en)
            st.session_state.story_hi = translator_hi.translate(story_en)

            # 3. Save MP3 for each language (full story)
            for lang_code, text_key, audio_key in [
                ("en", "story_en", "audio_en"),
                ("te", "story_te", "audio_te"),
                ("hi", "story_hi", "audio_hi")
            ]:
                text = st.session_state[text_key]
                if text.strip():
                    tts = gTTS(text=text, lang=lang_code)
                    path = os.path.join("static", f"story_{lang_code}.mp3")
                    tts.save(path)
                    st.session_state[audio_key] = path
                else:
                    st.session_state[audio_key] = ""

            # 4. Store English explanation
            st.session_state.explanation_en = explanation_en

            # 5. Translate explanation to Telugu & Hindi
            st.session_state.explanation_te = translator_te.translate(explanation_en)
            st.session_state.explanation_hi = translator_hi.translate(explanation_en)

            # 6. Reset flags
            st.session_state.show_explanation = False
            st.session_state.generate_flag = False


# ---- Display: Full Story in 3 Languages with Audio Players ----
if st.session_state.story_en:
    # Show appropriate animation for the subject
    st.markdown(f"<h4>📖 {subject} Story in English</h4>", unsafe_allow_html=True)
    if animation:
        st_lottie(animation, height=150, key=f"anim_en_{subject}")
    st.write(st.session_state.story_en)
    if os.path.exists(st.session_state.audio_en):
        st.audio(open(st.session_state.audio_en, "rb").read(), format="audio/mp3")
    else:
        st.info("English audio not available.")
    st.markdown("---", unsafe_allow_html=True)

    st.markdown(f"<h4>📖 {subject} Story (తెలుగు)</h4>", unsafe_allow_html=True)
    if animation:
        st_lottie(animation, height=150, key=f"anim_te_{subject}")
    st.write(st.session_state.story_te)
    if os.path.exists(st.session_state.audio_te):
        st.audio(open(st.session_state.audio_te, "rb").read(), format="audio/mp3")
    else:
        st.info("Telugu audio not available.")
    st.markdown("---", unsafe_allow_html=True)

    st.markdown(f"<h4>📖 {subject} Story (हिन्दी)</h4>", unsafe_allow_html=True)
    if animation:
        st_lottie(animation, height=150, key=f"anim_hi_{subject}")
    st.write(st.session_state.story_hi)
    if os.path.exists(st.session_state.audio_hi):
        st.audio(open(st.session_state.audio_hi, "rb").read(), format="audio/mp3")
    else:
        st.info("Hindi audio not available.")
    st.markdown("---", unsafe_allow_html=True)

    # Show Explanation button
    if st.button("🔍 Show Explanation in 3 Languages"):
        st.session_state.show_explanation = True


# ---- Display: Explanation in 3 Languages ----
if st.session_state.show_explanation:
    st.markdown("<h4>🔬 Concept Explanation</h4>", unsafe_allow_html=True)

    st.markdown("**English Explanation:**")
    st.write(st.session_state.explanation_en)
    st.markdown("---", unsafe_allow_html=True)

    st.markdown("**తెలుగు వివరణ (Telugu Explanation):**")
    st.write(st.session_state.explanation_te)
    st.markdown("---", unsafe_allow_html=True)

    st.markdown("**हिन्दी व्याख्या (Hindi Explanation):**")
    st.write(st.session_state.explanation_hi)
