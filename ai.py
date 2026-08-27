from google import genai

from brain.config import GEMINI_API_KEY


# Create Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY
)


# Gemini model
MODEL = "gemini-2.5-flash"


def ask_ai(prompt):

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        if response.text:
            return response.text.strip()

        return "I didn't receive a response from Gemini."

    except Exception as e:

        print(f"❌ Gemini API error: {e}")

        return (
            "I'm having trouble connecting "
            "to Gemini right now."
        )