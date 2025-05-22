from gtts import gTTS
import io

def generate_audio(text: str, lang_code: str, filename_prefix: str) -> bytes:
    """
    Generate speech audio from text using Google Text-to-Speech (gTTS).
    Returns audio data as bytes (mp3 format).

    Args:
        text (str): The text to convert to speech.
        lang_code (str): Language code for speech (e.g., 'en', 'te', 'hi').
        filename_prefix (str): Prefix for the audio file (used internally if saving).

    Returns:
        bytes: Audio content in MP3 format.
    """
    if not text or text.strip() == "":
        raise ValueError("No text provided for TTS generation")

    try:
        tts = gTTS(text=text, lang=lang_code)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes.read()
    except Exception as e:
        # Log or handle error here if needed
        raise RuntimeError(f"TTS generation failed: {e}")
