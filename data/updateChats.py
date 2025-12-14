from models import ChatIdentifier
from data.client import MongoClientSingleton
from typing import Optional 

# class ChatIdentifier(BaseModel):
#     userId: int
#     threadId: int

#update the object in chat collection aysnc
def updateChats(chatIdentifier: ChatIdentifier, summary: Optional[str]) -> None:
    # empty the recentChats List and patch with new summary
    client = MongoClientSingleton.get_client()    
    db = client["SDLC_Nexus"]
    collection = db["chats"]

    result = collection.update_one(
        {"userId": chatIdentifier.userId, "threadId": chatIdentifier.threadId},
        {
            "$set": {
                "recentChats": [],
                "summary": summary
            }
        }
    )

    if result.matched_count == 0:
        raise RuntimeError("No chat thread found for given userId and threadId")