from dotenv import load_dotenv
load_dotenv()   
#load a file
from srs_phase import loadFile 
from srs_phase import embeddings 
from srs_phase import chunking 
from vectorDb import uploadEmbeddings

def uploadInVedctorDb(filePath):
    
    document = loadFile.loadPdf(filePath) 

    #do chunking
    chunks = chunking.spiltDoc(document) 

    # #create embeddings 
    # vectors = embeddings.createEmbedings(chunks) 

    #create and store 
    uploadEmbeddings.uploadEmbbedings(chunks) 
    print("Upload in vector db complete")