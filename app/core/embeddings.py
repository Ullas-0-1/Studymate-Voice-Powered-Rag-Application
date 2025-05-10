# # app/core/embeddings.py

# import fitz  # PyMuPDF
# from sentence_transformers import SentenceTransformer
# import chromadb
# from chromadb.config import Settings
# from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# # Initialize embedding model
# embedder = SentenceTransformer('all-MiniLM-L6-v2')
# embedding_fn = SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L6-v2')

# # Initialize Chroma DB client


# from chromadb.config import Settings
# from chromadb import PersistentClient

# client = PersistentClient(path="vector_store")


# collection = client.get_or_create_collection("studymate", embedding_function=embedding_fn)

# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with fitz.open(pdf_path) as doc:
#         for page in doc:
#             text += page.get_text()
#     return text

# def process_and_store_pdf(pdf_path):
#     text = extract_text_from_pdf(pdf_path)
#     chunks = [text[i:i+500] for i in range(0, len(text), 500)]  # naive chunking
#     metadatas = [{"source": pdf_path, "chunk_id": idx} for idx in range(len(chunks))]
#     ids = [f"{pdf_path}_chunk_{idx}" for idx in range(len(chunks))]
    
#     collection.add(documents=chunks, metadatas=metadatas, ids=ids)
#     #collection.persist()  not required doirectlt does it

import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import os

# Initialize embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')
embedding_fn = SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L6-v2')

# Initialize Chroma DB client
from chromadb import PersistentClient
client = PersistentClient(path="vector_store")
collection = client.get_or_create_collection("studymate", embedding_function=embedding_fn)

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# def process_and_store_pdf(pdf_path):
#     text = extract_text_from_pdf(pdf_path)
#     chunks = [text[i:i+500] for i in range(0, len(text), 500)]  # naive chunking
#     metadatas = [{"source": pdf_path, "chunk_id": idx} for idx in range(len(chunks))]
#     ids = [f"{pdf_path}_chunk_{idx}" for idx in range(len(chunks))]
    
#     collection.add(documents=chunks, metadatas=metadatas, ids=ids)

def process_and_store_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]  # Better chunk size
    
    # USE ONLY FILENAME (not full path)
    filename = os.path.basename(pdf_path)  # "NoSQL_end_term.pdf"
    metadatas = [{"source": filename, "chunk_id": idx} for idx in range(len(chunks))]
    
    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=[f"{filename}_chunk_{idx}" for idx in range(len(chunks))]
    )