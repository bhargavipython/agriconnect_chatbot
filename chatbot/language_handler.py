from langdetect import detect
from deep_translator import GoogleTranslator

# 🌐 Detect original language
def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

# 🌐 Translate input to English for processing
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

# 🌐 Translate response back to user's original language
def translate_to_original(text, original_lang):
    try:
        if original_lang != "en":
            return GoogleTranslator(source='en', target=original_lang).translate(text)
        return text
    except:
        return text
