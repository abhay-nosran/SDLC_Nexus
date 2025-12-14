from typing import Union
from fastapi import FastAPI , UploadFile , File ,HTTPException
from uploadFile.uploadFile import upload_pdf_to_supabase
app = FastAPI()
import os 
from dotenv import load_dotenv
from upload import uploadInVedctorDb
load_dotenv()   
from pathlib import Path
import time 
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest , ChatResponse , ChatIdentifier
from service.getResponse import getResponse 
from service.getChats import getChats
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/uploadFile/")
async def uploadFile(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    uploads_dir = Path(__file__).parent / "uploads"
    uploads_dir.mkdir(exist_ok=True)

    # Extract file info
    original_name = Path(file.filename).stem      # without extension
    ext = Path(file.filename).suffix              # .pdf

    # Create timestamped file name
    timestamp = int(time.time())
    new_filename = f"{original_name}_{timestamp}{ext}"
    local_file_path = uploads_dir / new_filename

    # Read bytes and save locally
    file_bytes = await file.read()
    with open(local_file_path, "wb") as f:
        f.write(file_bytes)

    # Upload to Supabase using renamed file
    key = upload_pdf_to_supabase(
        os.getenv("SUPA_STORAGE_BUCKET"),
        file_bytes,
        new_filename                           # use new filename here
    )

    # Send the renamed file to vector DB
    uploadInVedctorDb(local_file_path)

    return {
        "uploaded_file": new_filename,
        "storage_key": key
    }


@app.post("/chat/", response_model=ChatResponse)
async def getResponse_route(chatQuery: ChatRequest):
    try:
        response = await getResponse(chatQuery)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/threads/{userId}/{threadId}")
def fetchChats(userId : int,threadId : int ):

    chatIdentifier = ChatIdentifier(userId=userId , threadId=threadId)
    frontend_chats = getChats(chatIdentifier)

    return frontend_chats