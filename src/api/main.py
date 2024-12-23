# api/main.py

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from backend.interfaces import IVectorStore, ILLMService
from backend.dependencies import get_vector_store, get_llm_service
from backend.generator import generate_response
from backend.data_loader import process_documents
import logging

logger = logging.getLogger("FastAPI")

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class UpdateRequest(BaseModel):
    content: str

@app.post("/aks")
def ask_question(request: QueryRequest, 
                 vector_store: IVectorStore = Depends(get_vector_store), 
                 llm_service: ILLMService = Depends(get_llm_service)):
    try:    
        query = request.query
        logger.info(f"Received query: {query}")
        response = generate_response(query, vector_store, llm_service)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Error processing request")
    
@app.post("/upload")
def upload_document(request: UpdateRequest, 
                    vector_store: IVectorStore = Depends(get_vector_store)):
    try:
        content = request.content
        logger.info(f"Received content: {content}")
        process_documents(content, vector_store)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Error processing request")
    
@app.get("/", summary="Root endpoint")
def read_root():
    """
    Root endpoint to verify that the API is running.
    """
    return {"message": "Welcome to the RAG FastAPI Application!"}