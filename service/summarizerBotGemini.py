from google import genai
from google.genai import types
from models import MongoContext

from dotenv import load_dotenv
load_dotenv() 

def summarizerBot(mongoContext: MongoContext) -> str:
    """
    Creates a reusable long-term memory summary that captures:
    - User goals and preferences
    - Important information exchanged
    - Assistant suggestions or steps given
    - Pending questions or unresolved tasks
    """

    # Build text history for summarization
    history_text = ""

    if mongoContext.summary:
        history_text += f"Previous summary:\n{mongoContext.summary}\n\n"

    if mongoContext.recentChats:
        history_text += "Recent chats:\n"
        for msg in mongoContext.recentChats:
            history_text += f"{msg.role}: {msg.text}\n"

    # Initialize Gemini client
    client = genai.Client()  # API key must be set in env: GEMINI_API_KEY / GOOGLE_API_KEY

    # System prompt
    system_instruction = (
        "You are a memory compression assistant. Convert the chat history into a reusable summary "
        "that preserves continuity for future conversations. Include only:\n"
        "- User goals and intentions\n"
        "- Key facts and constraints\n"
        "- Assistant suggestions or results\n"
        "- Pending questions / tasks\n"
        "Avoid storytelling, opinions, chit-chat, or filler text."
    )

    # Call Gemini model
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction
        ),
        contents=f"Summarize this chat history:\n{history_text}"
    )

    return response.text


if __name__ == "__main__" :
    text = summarizerBot(MongoContext(summary="my name is abhay"))
    print(text) 