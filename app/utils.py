
import fitz  # PyMuPDF
import openai
import os

# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ''
    for page in doc:
        text += page.get_text()
    return text

def get_resume_score(text):
    """Use OpenAI's GPT model to evaluate a resume and assign a score."""
    MAX_LENGTH = 2000  # Max token limit for OpenAI models
    if len(text) > MAX_LENGTH:
        text = text[:MAX_LENGTH]  # Truncate text if too long

    prompt = f"Evaluate this resume:\n\n{text}\n\nGive a score out of 100."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        # Extract the score from the response
        score = ''.join(filter(str.isdigit, response['choices'][0]['message']['content']))
        
        if score:
            return int(score)  # Return score if found
        else:
            return 50  # Return a default score if no score is found
    except Exception as e:
        print(f"Error while fetching the score: {e}")
        return 50  # Return a default score in case of error
