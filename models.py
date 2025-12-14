from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime , timezone

class ChatIdentifier(BaseModel):
    userId: int
    threadId: int

class Context(BaseModel):
    mongoContext : Optional[MongoContext] = None
    ragVectors: Optional[List[str]] = None  # List of embeddings

class MongoContext(BaseModel) :
    recentChats : Optional[List[Chat]] = None
    summary : Optional[str] = None

class ChatRequest(BaseModel):
    query: str
    chatIdentifier: ChatIdentifier

class Chat(BaseModel) : 
    text : str 
    role : str
    timestamp : datetime = Field(default_factory=datetime.now(timezone.utc))

class ChatResponse(BaseModel):
    content: str
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))

class ChatBotInput(BaseModel):
    query : str 
    context : Context

