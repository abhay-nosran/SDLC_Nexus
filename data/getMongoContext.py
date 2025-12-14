from models import ChatIdentifier , MongoContext ,Chat
from data.client import MongoClientSingleton


# class MongoContext(BaseModel) :
#     recentChats : Optional[List[Chat]] 
#     summary : Optional[str]

# class Chat(BaseModel) : 
#     text : str 
#     role : str
#     timestamp : datetime = Field(default_factory=datetime.utcnow)

# class ChatIdentifier(BaseModel):
#     userId: int
#     threadId: int

def getMongoContext(input: ChatIdentifier) -> MongoContext:
    client = MongoClientSingleton.get_client()
    
    db = client["SDLC_Nexus"]
    collection = db["chats"]

    document = collection.find_one(
        {"userId": input.userId, "threadId": input.threadId},
        {"_id": 0, "recentChats": 1, "summary": 1}
    )

    if document is None:
        return MongoContext(recentChats=None, summary=None)

    raw_recent = document.get("recentChats", [])
    recentChats = [Chat(**chat) for chat in raw_recent] if raw_recent else None

    return MongoContext(
        recentChats=recentChats,
        summary=document.get("summary")
    )

if __name__ == "__main__" :
    data = {"userId" : 1 ,"threadId" : 1 }
    dummy = ChatIdentifier(**data) 
    t = getMongoContext(dummy) 
    print(t) 