from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.qa_service import query_documents
from app.core.embeddings import process_and_store_pdf
import os
from typing import Optional

router = APIRouter()

@router.post("/")
async def query(
    question: str,
    file: Optional[UploadFile] = File(None)  # PDF is optional
):
    try:
        # Process new upload if provided
        if file:
            if not file.filename.lower().endswith(".pdf"):
                raise HTTPException(400, "Only PDF files supported")
            
            # Save and process PDF
            file_path = f"uploads/{file.filename}"
            os.makedirs("uploads", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(await file.read())
            
            process_and_store_pdf(file_path)
            
            # Force immediate use of this document
            answer = await query_documents(question, use_only_this_doc=file.filename)
        else:
            # Search all documents in ChromaDB
            answer = await query_documents(question)
        
        return {"answer": answer}
    
    except Exception as e:
        raise HTTPException(500, str(e))