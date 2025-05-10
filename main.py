from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.query import router as query_router

app = FastAPI(
    title="StudyMateGPT",
    description="Multilingual academic assistant using RAG",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to StudyMate!"}

# Include routers
app.include_router(upload_router, prefix="/upload", tags=["Upload"])
app.include_router(query_router, prefix="/query", tags=["Query"])