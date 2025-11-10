# voice_input.py
import speech_recognition as sr

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now!")
        audio = recognizer.listen(source)
        try:
            print("🧠 Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"✅ Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"❌ Could not request results: {e}")
            return None
