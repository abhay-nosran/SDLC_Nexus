import os 
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

url = "https://9d98e0f5-6842-4d82-bec6-ab99661358fa.eu-central-1-0.aws.cloud.qdrant.io"

def uploadEmbbedings(chunks) :
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    qdrant = QdrantVectorStore.from_documents(
        chunks,
        embeddings,
        api_key = os.environ.get("QDRANT_API_KEY"),
        url=url,
        prefer_grpc=True,
        collection_name="my_documents",
    )
    

