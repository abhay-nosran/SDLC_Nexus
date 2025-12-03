import os 
from dotenv import load_dotenv
load_dotenv()   
from pinecone import Pinecone

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = "test-index" 



