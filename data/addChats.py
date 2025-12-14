from models import Chat, ChatIdentifier
from typing import List
from data.client import MongoClientSingleton

# class ChatIdentifier(BaseModel):
#     userId: int
#     threadId: int

# class Chat(BaseModel) : 
#     text : str 
#     role : str
#     timestamp : datetime = Field(default_factory=datetime.utcnow)

def addChats(chatIdentifier: ChatIdentifier, chats: List[Chat]):
    """
    Appends chat messages to both `chats` and `recentChats` arrays
    inside the `chats` collection of SDLC_Nexus DB.
    Creates the document if not present.
    """

    client = MongoClientSingleton.get_client()
    db = client["SDLC_Nexus"]
    collection = db["chats"]

    # Convert Pydantic Chat models -> dict for MongoDB
    chat_dicts = [chat.dict() for chat in chats]

    collection.update_one(
        {"userId": chatIdentifier.userId, "threadId": chatIdentifier.threadId},
        {
            "$push": {
                "chats": {"$each": chat_dicts},
                "recentChats": {"$each": chat_dicts}
            },
            "$setOnInsert": {
                "summary": None
            }
        },
        upsert=True  # creates document if missing
    )
