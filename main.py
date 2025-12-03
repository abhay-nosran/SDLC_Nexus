from typing import Union
from fastapi import FastAPI , UploadFile , File ,HTTPException

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/uploadFile/")
async def uploadFile(file : UploadFile = File(...)) : 
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    with open(f"uploads/{file.filename}","wb") as f :
        f.write(await file.read()) 

    return {"uploaded file" : file.filename } 