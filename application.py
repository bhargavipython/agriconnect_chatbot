from flask import Flask, request, render_template, send_from_directory
import os

# ✅ Import chatbot engines
from chatbot.qa_engine import ask_question_from_pdf
from chatbot.web_search import search_web
from chatbot.excel_engine import load_excel, answer_excel_question
from chatbot.voice_input import get_voice_input  # Voice to text
from chatbot.text_to_speech import convert_text_to_speech  # ✅ ElevenLabs TTS

# ✅ Translation modules
from chatbot.language_handler import detect_language, translate_to_english, translate_to_original

application = Flask(__name__)
uploaded_excel_df = None
uploaded_pdf_path = None

# 🌐 UI translations
translations = {
    "en": {
        "select_lang": "🌍 Select Language:",
        "greeting": "👋 Hello! Upload a PDF, Excel file or ask your farming question below.",
        "info": "🌐 You can ask in any language – we’ll translate and answer it!",
        "question": "❓ Question:",
        "answer": "✅ Answer:",
        "pdf": "📄 PDF Q&A",
        "web": "🌐 Web Search",
        "excel": "📊 Excel Calc",
        "voice": "🎤 Ask via Voice",
        "placeholder": "Type your farming question in any language...",
        "btn": "🚀 Get Answer"
    },
    "te": {
        "select_lang": "🌍 భాషను ఎంచుకోండి:",
        "greeting": "👋 హలో! PDF, Excel ఫైల్ అప్‌లోడ్ చేయండి లేదా మీ వ్యవసాయ ప్రశ్నను అడగండి.",
        "info": "🌐 మీరు ఏ భాషలోనైనా అడగవచ్చు – మేము అనువదించి సమాధానం ఇస్తాము!",
        "question": "❓ ప్రశ్న:",
        "answer": "✅ సమాధానం:",
        "pdf": "📄 PDF ప్రశ్నలు",
        "web": "🌐 వెబ్ సెర్చ్",
        "excel": "📊 ఎక్సెల్ లెక్కలు",
        "voice": "🎤 వాయిస్ ద్వారా అడగండి",
        "placeholder": "మీ వ్యవసాయ ప్రశ్నను టైప్ చేయండి లేదా వాయిస్ ఉపయోగించండి...",
        "btn": "🚀 సమాధానం పొందండి"
    },
    "hi": {
        "select_lang": "🌍 भाषा चुनें:",
        "greeting": "👋 नमस्ते! PDF, Excel फ़ाइल अपलोड करें या अपना कृषि प्रश्न पूछें।",
        "info": "🌐 आप किसी भी भाषा में पूछ सकते हैं – हम अनुवाद कर उत्तर देंगे!",
        "question": "❓ प्रश्न:",
        "answer": "✅ उत्तर:",
        "pdf": "📄 PDF प्रश्नोत्तर",
        "web": "🌐 वेब खोज",
        "excel": "📊 एक्सेल कैलकुलेशन",
        "voice": "🎤 आवाज़ से पूछें",
        "placeholder": "अपना कृषि प्रश्न टाइप करें या वॉयस इनपुट दें...",
        "btn": "🚀 उत्तर प्राप्त करें"
    }
}

@application.route("/", methods=["GET", "POST"])
def index():
    global uploaded_excel_df, uploaded_pdf_path
    answer = ""
    question = ""
    audio_file = None
    selected_lang = request.form.get("lang", request.args.get("lang", "en"))

    if selected_lang not in translations:
        selected_lang = "en"

    t = translations[selected_lang]

    if request.method == "POST":
        use_pdf = request.form.get("use_pdf") == "on"
        use_excel = request.form.get("use_excel") == "on"
        use_web = request.form.get("use_web") == "on"
        use_voice = request.form.get("use_voice") == "on"

        # ✅ PDF Upload
        if use_pdf and "pdf_file" in request.files:
            pdf_file = request.files["pdf_file"]
            if pdf_file.filename:
                uploaded_pdf_path = os.path.join("uploads", pdf_file.filename)
                pdf_file.save(uploaded_pdf_path)

        # ✅ Excel Upload
        if use_excel and "excel_file" in request.files:
            excel_file = request.files["excel_file"]
            if excel_file.filename:
                excel_path = os.path.join("uploads", excel_file.filename)
                excel_file.save(excel_path)
                uploaded_excel_df = load_excel(excel_path)

        # ✅ Voice Input
        if use_voice and "voice_file" in request.files:
            voice_file = request.files["voice_file"]
            if voice_file.filename:
                voice_path = os.path.join("uploads", voice_file.filename)
                voice_file.save(voice_path)
                question = get_voice_input(voice_path)

        # ✅ Text fallback
        if not question:
            question = request.form.get("question", "")

        if question:
            try:
                original_lang = detect_language(question)
                question_en = translate_to_english(question)

                # ✅ Answer logic
                if use_excel and uploaded_excel_df is not None:
                    answer_en = answer_excel_question(uploaded_excel_df, question_en)
                elif use_pdf and uploaded_pdf_path:
                    answer_en = ask_question_from_pdf(uploaded_pdf_path, question_en)
                elif use_web:
                    answer_en = search_web(question_en)
                else:
                    answer_en = "❌ No data source selected."

                answer = translate_to_original(answer_en, original_lang)

                # ✅ ElevenLabs TTS
                audio_path = convert_text_to_speech(answer)
                if audio_path:
                    audio_file = os.path.basename(audio_path)  # just filename

            except Exception as e:
                answer = f"❌ Error: {str(e)}"
                audio_file = None

    return render_template("index.html",
                           answer=answer,
                           question=question,
                           t=t,
                           selected_lang=selected_lang,
                           audio_file=audio_file)

# ✅ Serve audio safely
@application.route("/static/audio/<filename>")
def serve_audio(filename):
    return send_from_directory("static/audio", filename)

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("static/audio", exist_ok=True)
    application.run(debug=True)
