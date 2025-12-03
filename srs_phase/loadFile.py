from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

#load file 
def loadPdf(filePath):
    loader = PyPDFLoader(filePath) 
    file = loader.load() 
    return file 

filePath = Path(__file__).parent / "sample.pdf" 

