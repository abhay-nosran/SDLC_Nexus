from service.getContext import getContext
from service.chatBot import chatBot 
from models import ChatRequest , ChatResponse , ChatBotInput , Chat , ChatIdentifier
from service.addChats import addChats 
from service.summarizer import summarizer
import asyncio 
from datetime import datetime , timezone

from dotenv import load_dotenv
load_dotenv() 

# class ChatRequest(BaseModel):
#     query: str
#     chatIdentifier: ChatIdentifier

# class ChatBotInput(BaseModel):
#     query : str 
#     context : Context

# class ChatResponse(BaseModel):
#     content: str
#     timestamp: datetime = Field(default_factory=datetime.utcnow)

# class Chat(BaseModel) : 
#     text : str 
#     role : str
#     timestamp : datetime = Field(default_factory=datetime.utcnow)

async def getResponse_async(chat):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: getResponse(chat))

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)   # separate threads

async def getResponse(chat : ChatRequest) -> ChatResponse:

    userChat = Chat(text=chat.query , role = "user" , timestamp=datetime.now(timezone.utc))
    # 1 call getContext 
    # 2 call chatbot 
    context = getContext(chat.chatIdentifier) # type : Context 
    chatInput = ChatBotInput(query = chat.query , context = context)
    response = chatBot(chatInput)

    # add query and response to mongo recentChats and chats using an async worker
    aiChat = Chat(text = response.content , role="model" , timestamp=response.timestamp)

    loop = asyncio.get_running_loop()

    # Task 1 — addChats (always runs)
    loop.run_in_executor(executor, addChats, chat.chatIdentifier, userChat, aiChat)
    
    # Task 2 — summarizer (only when needed)
    if context.mongoContext and context.mongoContext.recentChats and len(context.mongoContext.recentChats) > 4:
        loop.run_in_executor(executor, summarizer, chat.chatIdentifier, context.mongoContext)


    return response 

if __name__ == "__main__" :
    chat = ChatRequest(query="what is my name" , chatIdentifier=ChatIdentifier(userId=1,threadId=1)) 
    response = asyncio.run(getResponse_async(chat))  # must be async
    print(response)