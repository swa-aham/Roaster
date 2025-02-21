import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"  # Base URL without the key

def get_gemini_response(text):
    try:
        # Construct the URL with the API key
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"

        prompt = f"""
        Summarize the contents of the given text:
        {text}
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
    
    
text = "The moon hung low in the sky, casting a pale glow over the sleepy village. A soft breeze rustled the leaves of the old oak tree at the edge of town. Ellie stood at the base of the tree, holding an old, tattered map in her hands. Her heart raced as she traced the mysterious symbols with her fingers. Legends told of hidden treasures buried deep beneath the earth, but no one had ever dared to search for them. The map had been passed down through generations, but no one knew what had happened to the last person who sought its secrets. Tonight, Ellie was determined to uncover the truth. She took a deep breath, tucking the map into her coat, and began walking toward the forest. The night was quiet, save for the sound of her footsteps on the gravel path. What lay ahead was unknown, but Ellie could feel the weight of destiny on her shoulders."


# value = os.getenv("value")
# # print(value)
    
print(get_gemini_response(text))