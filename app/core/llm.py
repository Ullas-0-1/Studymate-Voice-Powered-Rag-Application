import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_answer(prompt: str, context: str = None) -> str:
    """Generate answer using Gemini with optional context"""
    try:
        if context:
            full_prompt = f"""You are StudyMateGPT, an AI assistant for students. 
            Use the following context to answer the question. If you don't know, say so.
            
            Context: {context}
            
            Question: {prompt}
            
            Answer:"""
        else:
            full_prompt = f"""You are StudyMateGPT, an AI assistant for students. 
            Answer the following question helpfully and simply.
            
            Question: {prompt}
            
            Answer:"""
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Gemini API error: {str(e)}")