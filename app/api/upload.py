# app/api/upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.embeddings import process_and_store_pdf

router = APIRouter()

@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        process_and_store_pdf(file_path)
        return {"message": f"{file.filename} uploaded and processed successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
