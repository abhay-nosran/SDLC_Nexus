from langchain_google_genai import GoogleGenerativeAIEmbeddings

def createEmbedings(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectors = embeddings.embed_documents(chunks)
    return vectors 

