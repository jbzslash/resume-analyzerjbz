import fitz  # PyMuPDF
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ''
    for page in doc:
        text += page.get_text()
    return text

def get_resume_score(text):
    prompt = f"Evaluate this resume:\n\n{text}\n\nGive a score out of 100."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    score = ''.join(filter(str.isdigit, response['choices'][0]['message']['content']))
    return int(score) if score else 50
