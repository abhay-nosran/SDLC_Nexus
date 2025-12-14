from data.getChats import getChats as getChats_db
from typing import List 
from models import  ChatIdentifier

def getChats(chatIdentifier : ChatIdentifier) -> List[dict]:
    formatted = []
    chats = getChats_db(chatIdentifier)
    for chat in chats:
        role = "user" if chat.role == "user" else "bot"

        formatted.append({
            "role": role,
            "text": chat.text,
            "timestamp": chat.timestamp
        })

    return formatted
