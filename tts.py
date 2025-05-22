from gtts import gTTS
import os

def generate_audio(text, lang_code, filename):
    tts = gTTS(text=text, lang=lang_code)
    filepath = f"audio/{filename}.mp3"
    os.makedirs("audio", exist_ok=True)
    tts.save(filepath)
    return filepath
