import streamlit as st
from story_generator import generate_story
from translator import translate
from tts import generate_audio

# Read the API key from Streamlit secrets
api_key = st.secrets["TOGETHER_API_KEY"]


# Custom CSS to style headers and page
st.markdown(
    """
    <style>
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #4a90e2;
        text-align: center;
    }
    .section-header {
        color: #1177cc;
        font-weight: bold;
        font-size: 28px;
        margin-top: 30px;
    }
    .footer {
        font-size: 12px;
        color: gray;
        text-align: center;
        margin-top: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">📚 AI Educational Story App</div>', unsafe_allow_html=True)

# Input section in sidebar for better layout
with st.sidebar:
    st.header("Select Options")
    grades = ["1", "2", "3", "4", "5", "6", "7"]
    subjects = ["Math", "Science", "English", "EVS"]
    languages = {
        "English": "en",
        "Telugu": "te",
        "Hindi": "hi",
        "Tamil": "ta",
        "Kannada": "kn"
    }

    grade = st.selectbox("Grade", grades)
    subject = st.selectbox("Subject", subjects)
    concept = st.text_input("Concept")
    language = st.selectbox("Language", list(languages.keys()))
    generate_btn = st.button("Generate Story & Explanation")

st.markdown("---")

if generate_btn and concept.strip():
    with st.spinner("Generating story and explanation..."):
        # Generate story
        story_prompt = (
            f"Write a fun, creative story for grade {grade} students that teaches the concept "
            f"'{concept}' in {subject}, but do not directly say the concept name. "
            "Make it interesting and easy to understand for kids."
        )
        story_en = generate_story(story_prompt, grade, subject, api_key)

        # Generate explanation (direct, no story)
        explanation_prompt = (
            f"Explain the concept '{concept}' from {subject} in simple, clear, and brief terms for grade {grade} students. "
            "Do not tell a story or use analogies; just explain the concept directly."
        )
        explanation_en = generate_story(explanation_prompt, grade, subject, api_key)

    # Show results in two columns: English & Selected language
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">📖 Story in English</div>', unsafe_allow_html=True)
        with st.expander("Show Story"):
            st.write(story_en)
            audio_en_story = generate_audio(story_en, "en", "english_story")
            st.audio(audio_en_story)

        st.markdown('<div class="section-header">🧠 Explanation in English</div>', unsafe_allow_html=True)
        with st.expander("Show Explanation"):
            st.write(explanation_en)
            audio_en_exp = generate_audio(explanation_en, "en", "english_explanation")
            st.audio(audio_en_exp)

    with col2:
        if language != "English":
            st.markdown(f'<div class="section-header">📖 Story in {language}</div>', unsafe_allow_html=True)
            with st.expander(f"Show Story in {language}"):
                story_translated = translate(story_en, languages[language])
                st.write(story_translated)
                audio_trans_story = generate_audio(story_translated, languages[language], "translated_story")
                st.audio(audio_trans_story)

            st.markdown(f'<div class="section-header">🧠 Explanation in {language}</div>', unsafe_allow_html=True)
            with st.expander(f"Show Explanation in {language}"):
                explanation_translated = translate(explanation_en, languages[language])
                st.write(explanation_translated)
                audio_trans_exp = generate_audio(explanation_translated, languages[language], "translated_explanation")
                st.audio(audio_trans_exp)
        else:
            st.info("English is selected as the language, so content is shown on the left.")

else:
    st.info("Please enter a concept and click 'Generate Story & Explanation' to begin.")

st.markdown('<div class="footer">Developed with ❤️ by YourName</div>', unsafe_allow_html=True)
