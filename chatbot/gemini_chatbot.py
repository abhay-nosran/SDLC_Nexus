# from google import genai

# # The client gets the API key from the environment variable `GEMINI_API_KEY`.
# client = genai.Client(api_key="")

# response = client.models.generate_content(
#     model="gemini-2.5-flash", contents="Explain how AI works in a few words"
# )
# print(response.text)

from google import genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# The model you confirmed is working
MODEL_NAME = "gemini-2.5-flash"

def chat_with_gemini(prompt):
    # Generate the response
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text.strip()

if __name__ == "__main__":
    print("Gemini Chatbot Ready!")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Chatbot: Goodbye! 👋")
            break

        reply = chat_with_gemini(user_input)
        print("Chatbot:", reply)
