from dotenv import load_dotenv
load_dotenv()   
#load a file
from srs_phase import loadFile 
from srs_phase import embeddings 
from srs_phase import chunking 
from vectorDb import uploadEmbeddings

document = loadFile.loadPdf(loadFile.filePath) 

#do chunking
chunks = chunking.spiltDoc(document) 

# #create embeddings 
# vectors = embeddings.createEmbedings(chunks) 

#create and store 
uploadEmbeddings.uploadEmbbedings(chunks) 