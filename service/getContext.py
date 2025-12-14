from models import Context , ChatIdentifier
from data.getMongoContext import getMongoContext 


# class ChatIdentifier(BaseModel):
#     userId: int
#     threadId: int

# class Context(BaseModel):
#     mongoContext : Optional[MongoContext]
#     ragVectors: Optional[List[str]]  # List of embeddings

# class MongoContext(BaseModel) :
#     recentChats : Optional[List[Chat]] 
#     summary : Optional[str]

# class Chat(BaseModel) : 
#     text : str 
#     role : str
#     timestamp : datetime = Field(default_factory=datetime.utcnow)

def getContext(input : ChatIdentifier) ->  Context:

    # 1 . call getMongoContext from data
    # 2 . call getRagContext from data (to be implemented later)

    mongoContext = getMongoContext(input) 

    return Context(mongoContext=mongoContext ,ragVectors=None )  









