import requests
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import streamlit as st
import os

# Load environment variables
load_dotenv()

# Get the API key from the .env file
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"  # Base URL without the key

def get_gemini_response(profile, lang=""):
    try:
        # Construct the URL with the API key
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"

        prompt = f"""
        You are a savage, witty professional roaster with a flair for humor, sarcasm, and punchy comebacks.
        Below is the content of my resume:
        {profile}
        
        Your Task: Based on the resume above, roast the profile aggressively (but still entertainingly) in under 300 words. Be brutally honest, creatively sarcastic, and hilariously critical — no holding back.

        📝 Formatting Instructions:
        Use Markdown only.
        Add bold, italics, inline code (if needed), and structured headings/subheadings.
        Include emojis liberally for humor and tone.
        Use bullet points or short, punchy paragraphs for rhythm and engagement.
        
        🎯 Tone Goals:
        Roasts should be funny, savage, and clever, not mean-spirited or offensive.
        Focus on contradictions, clichés, buzzwords, inflated titles, gaps, odd achievements, or anything that sounds too "corporate polished."
        Feel free to mock overused phrases like “results-driven”, “synergy”, “go-getter”, etc.
        Let the roasting begin. 🔥

        If the resume belongs to Soham Mandaviya, do not roast. Instead, praise him extravagantly as if he's the perfect blend of Elon Musk's vision, Leonardo da Vinci’s creativity, and The Rock’s work ethic. Make it epic, funny, and impressively over-the-top. Still use the same formatting and word limit.


        
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
