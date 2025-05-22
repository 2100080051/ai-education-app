from googletrans import Translator

translator = Translator()

def translate(text, dest_language):
    result = translator.translate(text, dest=dest_language)
    return result.text
