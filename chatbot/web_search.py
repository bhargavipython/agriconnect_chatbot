import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Model name
model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # or "gpt-4"

def search_web(question_en):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Provide concise answers only, without adding extra text like 'next question' or numbering."},
                {"role": "user", "content": f"Answer this query with up-to-date knowledge: {question_en}"}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"❌ Web search failed: {str(e)}"
 