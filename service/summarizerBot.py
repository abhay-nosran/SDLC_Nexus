from models import MongoContext
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()


# class MongoContext(BaseModel) :
#     recentChats : Optional[List[Chat]] = None
#     summary : Optional[str] = Node

def summarizerBot(mongoContext: MongoContext) -> str:
    """
    Creates a reusable long-term memory summary that captures:
    - User goals and preferences
    - Important information exchanged
    - Assistant suggestions or steps given
    - Pending questions or unresolved tasks
    """

    history_text = ""

    # Add previous summary first (foundation memory)
    if mongoContext.summary:
        history_text += f"Previous summary:\n{mongoContext.summary}\n\n"

    # Add recent chat messages (short-term context for update)
    if mongoContext.recentChats:
        history_text += "Recent chats:\n"
        for msg in mongoContext.recentChats:
            history_text += f"{msg.role}: {msg.text}\n"

    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.4,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    messages = [
        (
            "system",
            "You are a memory compression assistant. Convert the chat history into a compact summary "
            "that preserves information needed for future continuation of the conversation. "
            "Include:\n"
            "- User goals and intentions\n"
            "- Important facts or constraints discussed\n"
            "- Assistant guidance or solutions provided\n"
            "- Any unresolved questions or follow-up tasks\n"
            "Avoid dropping important details. No storytelling. No opinions. No formatting."
        ),
        (
            "human",
            f"Generate a reusable memory summary based on this history:\n{history_text}"
        ),
    ]

    ai_msg = model.invoke(messages)
    return ai_msg.content


if __name__ == "__main__" :
    summarizerBot(MongoContext(summary="my name is abhay"))