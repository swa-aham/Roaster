import requests
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the API key from the .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"  # Base URL without the key

def get_gemini_response(profile, lang=""):
    try:
        # Construct the URL with the API key
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"

        prompt = f"""
        You are a professional roaster. Here is the contents of my CV:
        {profile}
        
        Based on the above CV, roast the profile aggressively within 150 words.
        Use markdown format only. Do bold, italics, headings, subheadings, bullets, etc formatting wherever needed.
        Add emojis also to make it engaging.
        """

        if lang != "":
            prompt += f"""
            Use puns from {lang} movies, songs, books, literature, news, politics, idioms or any cultural or sarcastic contexts at appropriate positions.
            You can add the English translation in braces though.
        """

        response = requests.post(
            url,  # Use the complete URL with the API key appended
            headers={"Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": prompt}]}]}
        )
        response.raise_for_status()

        # Extract the text from the response using the updated structure
        result = response.json()
        if 'candidates' in result:
            # Access the 'text' field from the response structure
            generated_text = result['candidates'][0]['content']['parts'][0]['text']
            return generated_text
        else:
            return 'No candidates found in response.'

    except Exception as e:
        return f"An error occurred: {e}"

def read_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"An error occurred: {e}"
