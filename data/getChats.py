from models import ChatIdentifier , Chat 
from typing import List
from data.client import MongoClientSingleton
# class ChatIdentifier(BaseModel):
#     userId: int
#     threadId: int

# class Chat(BaseModel) : 
#     text : str 
#     role : str
#     timestamp : datetime = Field(default_factory=datetime.now(timezone.utc))



def getChats(chatIdentifier: ChatIdentifier) -> List[Chat]:

    client = MongoClientSingleton.get_client() 
    db = client["SDLC_Nexus"]
    collection = db["chats"]
    doc = collection.find_one({
        "userId": chatIdentifier.userId,
        "threadId": chatIdentifier.threadId
    })

    if not doc or "chats" not in doc:
        return []

    chat_list: List[Chat] = []
    for message in doc["chats"]:
        chat_list.append(Chat(**message))

    return chat_list


if __name__ == "__main__" :
    chats = getChats(ChatIdentifier(userId=1,threadId=1))
    print(chats)




