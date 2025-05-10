from app.core.embeddings import collection  # Import the Chroma collection
from sentence_transformers import SentenceTransformer
from typing import Optional



# app/core/rag_engine.py
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_relevant_chunks(query: str, restrict_to_doc: str = None, top_k: int = 3):
    try:
        # Generate query embedding
        query_embedding = embedder.encode(query).tolist()
        
        # Build filter (if restricting to one document)
        where_filter = {"source": restrict_to_doc} if restrict_to_doc else None
        
        # Search with both text and embedding
        results = collection.query(
            query_texts=[query],  # Text-based search
            query_embeddings=[query_embedding],  # Vector search
            n_results=top_k,
            where=where_filter
        )
        
        # Format results
        return [{
            'text': doc,
            'source': meta['source'],
            'score': score
        } for doc, meta, score in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )]
    
    except Exception as e:
        print(f"Retrieval error: {str(e)}")  # Debug log
        return []  # Return empty list on failure