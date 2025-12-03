from langchain_text_splitters import RecursiveCharacterTextSplitter

def spiltDoc(document):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(document)
    print(type(chunks[0]))
    return chunks