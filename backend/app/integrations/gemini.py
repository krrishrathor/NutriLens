import time

from google import genai

from app.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)

def generate_response(prompt: str) -> str:
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            if attempt == max_retries - 1:
                raise e

            wait_time = 2 ** attempt
            time.sleep(wait_time)
        