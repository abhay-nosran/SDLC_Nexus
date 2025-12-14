from dotenv import load_dotenv
load_dotenv()   
#load a file
from srs_phase import loadFile 
from srs_phase import embeddings 
from srs_phase import chunking 
from vectorDb import uploadEmbeddings

from pathlib import Path

def uploadInVedctorDb(filePath):
    
    document = loadFile.loadPdf(filePath) 

    #do chunking
    chunks = chunking.spiltDoc(document) 

    # #create embeddings 
    # vectors = embeddings.createEmbedings(chunks) 

    #create and store 
    uploadEmbeddings.uploadEmbbedings(chunks) 
    print("Upload in vector db complete")

if __name__ == "__main__":
    uploads_dir = Path(__file__).parent / "uploads"
    local_file_path = uploads_dir / "sample.pdf"
    print(local_file_path)
    uploadInVedctorDb(local_file_path) 