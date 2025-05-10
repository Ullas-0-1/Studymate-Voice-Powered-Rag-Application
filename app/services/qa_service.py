from app.core.rag_engine import retrieve_relevant_chunks
from app.core.llm import generate_answer
from typing import Optional

# app/services/qa_service.py
async def query_documents(question: str, use_only_this_doc: str = None):
    try:
        # Retrieve chunks (empty list if none found)
        relevant_chunks = retrieve_relevant_chunks(question, use_only_this_doc)
        
        if not relevant_chunks:
            print("No relevant chunks found!")  # Debug
            return generate_answer(question)  # Fallback to general knowledge
        
        # Build context from top chunks
        context = "\n\n---\n\n".join(
            f"From {chunk['source']} (relevance: {chunk['score']:.2f}):\n{chunk['text']}"
            for chunk in relevant_chunks
        )
        
        return generate_answer(question, context)
    
    except Exception as e:
        raise Exception(f"Query failed: {str(e)}")