from models import Chat , ChatIdentifier
import asyncio
from data.addChats import addChats as db_addChats
# class Chat(BaseModel) : 
#     text : str 
#     role : str
# timestamp : datetime = Field(default_factory=datetime.utcnow)

def addChats(chatIdentifier: ChatIdentifier, userChat: Chat, aiResponse: Chat):
    db_addChats(chatIdentifier, [userChat, aiResponse])


