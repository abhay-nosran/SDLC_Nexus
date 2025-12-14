from typing import Union
from fastapi import FastAPI , UploadFile , File ,HTTPException
from uploadFile.uploadFile import upload_pdf_to_supabase
app = FastAPI()
import os 
from dotenv import load_dotenv
from upload import uploadInVedctorDb
load_dotenv()   
from pathlib import Path

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/uploadFile/")
async def uploadFile(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    uploads_dir = Path(__file__).parent / "uploads"

    file_bytes = await file.read()
    local_file_path = uploads_dir / file.filename

    with open(local_file_path, "wb") as f:
        f.write(file_bytes)

    key = upload_pdf_to_supabase(os.getenv("SUPA_STORAGE_BUCKET"), file_bytes, file.filename)

    uploadInVedctorDb(local_file_path)  # pass correct path

    return {"uploaded_file": file.filename}