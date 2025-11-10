import os
from PyPDF2 import PdfReader
from chatbot.language_handler import translate_to_english
from difflib import SequenceMatcher

def normalize(text):
    return text.lower().strip().replace("?", "").replace(".", "").replace(",", "")

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def analyze_topic_from_pdf(pdf_path, user_topic):
    try:
        # Step 1: Translate to English
        user_topic_en = translate_to_english(user_topic)
        user_topic_norm = normalize(user_topic_en)

        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"

        # Step 2: Split into paragraphs or sections (assuming paragraphs separated by double newlines or single newlines)
        paragraphs = [p.strip() for p in full_text.replace('\n\n', '\n').split('\n') if p.strip()]

        # Step 3: Calculate similarity scores for all paragraphs
        scored_paragraphs = []
        for para in paragraphs:
            para_norm = normalize(para)
            score = similar(user_topic_norm, para_norm)
            scored_paragraphs.append((score, para))

        # Step 4: Sort by similarity score descending and select top 3
        scored_paragraphs.sort(key=lambda x: x[0], reverse=True)
        top_paragraphs = [para for score, para in scored_paragraphs[:3] if score > 0.1]  # Threshold to avoid irrelevant matches

        if top_paragraphs:
            # Return top matching paragraphs for complete topic information
            combined_content = '\n\n'.join(top_paragraphs)
            return combined_content.strip()
        else:
            return "❌ Uploaded PDF does not contain relevant information on the topic."

    except Exception as e:
        return f"❌ PDF Read Error: {str(e)}"

# Keep the old function for backward compatibility or rename
def ask_question_from_pdf(pdf_path, user_question):
    try:
        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"

        # Detect if PDF is in Q&A format
        if "Q:" in full_text and "A:" in full_text:
            # Use original Q&A logic
            user_question_en = translate_to_english(user_question)
            user_question_norm = normalize(user_question_en)

            q_blocks = full_text.split("Q:")
            best_match = ""
            best_score = 0.0
            best_answer = ""

            for block in q_blocks[1:]:
                if "A:" in block:
                    q_text, a_text = block.split("A:", 1)
                    q_norm = normalize(q_text)

                    score = similar(user_question_norm, q_norm)
                    if score > best_score:
                        best_score = score
                        best_match = q_text.strip()
                        next_q_index = a_text.find("\nQ:")
                        if next_q_index == -1:
                            next_q_index = a_text.find("Q:")
                        if next_q_index != -1:
                            best_answer = a_text[:next_q_index].strip()
                        else:
                            best_answer = a_text.strip()
                        best_answer = best_answer.rstrip('0123456789. ')

            if best_score > 0.7:
                return best_answer
            else:
                return "❌ Uploaded PDF does not contain a similar enough question."
        else:
            # Use topic analysis for general documents
            return analyze_topic_from_pdf(pdf_path, user_question)

    except Exception as e:
        return f"❌ PDF Read Error: {str(e)}"
