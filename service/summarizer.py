import asyncio
from service.summarizerBotGemini import summarizerBot
from data.updateChats import updateChats

def summarizer(chatIdentifier, mongoContext)->None:
   
    summary = summarizerBot(mongoContext)

    return updateChats(chatIdentifier,summary)