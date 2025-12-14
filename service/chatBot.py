from google import genai
from google.genai import types
from models import ChatBotInput, ChatResponse,  MongoContext
from datetime import datetime , timezone

# class ChatResponse(BaseModel):
#     content: str
#     timestamp: datetime = Field(default_factory=datetime.utcnow)

# class ChatBotInput(BaseModel):
#     query : str 
#     context : Context

def chatBot(input: ChatBotInput) -> ChatResponse:
    """
    SDLC Nexus chat model:
    Uses LLM with context memory (recentChats + summary) to generate a technical answer.
    Designed to act as a Senior Software Engineer helping with SDLC and software development.
    """

    client = genai.Client()  # requires GOOGLE_API_KEY / GEMINI_API_KEY in .env

    # Build contextual prompt
    context_text = ""

    mongo_ctx: MongoContext = input.context.mongoContext

    # Add memory summary
    if mongo_ctx and mongo_ctx.summary:
        context_text += f"Memory Summary:\n{mongo_ctx.summary}\n\n"

    # Add recent chats
    if mongo_ctx and mongo_ctx.recentChats:
        context_text += "Recent Chats:\n"
        for msg in mongo_ctx.recentChats:
            context_text += f"{msg.role}: {msg.text}\n"

    # System prompt for SDLC-focused assistant
    system_instruction = (
        """You are a senior software engineer assisting the user in designing and building software systems.

            Your responsibilities:
            - Provide clear, practical, and technically accurate guidance.
            - Focus on SDLC phases, system design, requirements analysis, backend and frontend engineering, API design, databases, cloud, DevOps, scalability, security, performance, testing, debugging, and best practices.
            - Keep responses structured, concise, and free of unnecessary storytelling.

            Memory rules:
            - You have access to a memory summary and recent chat messages. Use them only to maintain context and continuity.
            - If the user asks about previously shared personal information (e.g., name, preferences, interests), answer using memory only if the information is present.
            - Do not guess or fabricate any information. If memory does not contain the answer, reply: "I don't have that information yet."

            Safety and boundaries:
            - Do not engage in casual small talk, compliments, emotions, jokes, motivation, or role-playing.
            - If the user asks for something outside software engineering but the answer exists in memory (e.g., “what is my name”), answer factually.
            - If the user asks for something outside software engineering that is not available in memory, redirect politely back to software topics."""
    )

    # Build model input
    contents = (
        f"{context_text}\n"
        f"User Query:\n{input.query}"
    )

    # Call Gemini model
    llm_response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction
        ),
        contents=contents
    )

    # Return as ChatResponse Pydantic object
    return ChatResponse(
        content=llm_response.text,
        timestamp=datetime.now(timezone.utc)
    )
