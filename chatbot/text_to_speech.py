# text_to_speech.py
import requests
import os

ELEVENLABS_API_KEY = "sk_cc7f18f2e055e4364df280afd7264fcc388fe1ea863f6ab5"  
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  

def convert_text_to_speech(text, output_path="static/audio/generated_answer.mp3"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path
    else:
        print(f"❌ ElevenLabs API Error {response.status_code}: {response.text}")
        return None
