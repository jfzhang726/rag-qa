# api/main.py

from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.file_processors.processor_factory import FileProcessorFactory
from backend.interfaces import IVectorStore, ILLMService
from backend.dependencies import get_vector_store, get_llm_service, get_raw_file_storage, get_file_processor_factory
from backend.generator import generate_response
# from backend.data_loader import process_documents
from backend.models import FileStatus, Files
from backend.database import engine, AsyncSessionLocal, init_db
from sqlalchemy import insert, select, update
from sqlalchemy.exc import SQLAlchemyError
import uuid 
import os 
import logging

from backend.storage.base_storage import BaseStorage
from backend.storage.local_storage import LocalStorage
from backend.storage.s3_storage import S3Storage

logger = logging.getLogger("FastAPI")

app = FastAPI(title="RAG FastAPI Application", description="FastAPI application for RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class QueryRequest(BaseModel):
    query: str

class UpdateRequest(BaseModel):
    content: str

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     database_url = os.getenv("DATABASE_URL")
#     logger.info(f"Connecting to database: {database_url}")
#     await init_db()
#     logger.info("Database initialized.")
#     yield
#     await engine.dispose()

@app.on_event("startup")
async def on_startup():
    """
    Event handler for application startup.
    Initializes the database by creating necessary tables.
    """
    database_url = os.getenv("DATABASE_URL")
    logger.info(f"DATABASE_URL: {database_url}")  # Log the DATABASE_URL
    await init_db()
    logger.info("Database initialized.")

# @app.on_event("shutdown")
# async def on_shutdown():
#     """
#     Event handler for application shutdown.
#     Disposes of the engine to close database connections gracefully.
#     """
#     await engine.dispose()
#     logger.info("Database connections closed.")

@app.post("/api/ask", summary="Ask question")
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
    
@app.post("/api/upload", summary="Upload document")
async def upload_document(
    file: UploadFile = File(...),
    raw_file_storage: BaseStorage = Depends(get_raw_file_storage), 
    vector_store: IVectorStore = Depends(get_vector_store),
    file_processor_factory: FileProcessorFactory = Depends(get_file_processor_factory)
):
    
    try:
        logger.info(f"Received file: {file.filename}")
        file_extension = os.path.splitext(file.filename)[1]
        logger.info(f"File extension: {file_extension}")

        processor = file_processor_factory.get_processor(file_extension)

        file_uuid = str(uuid.uuid4())
        stored_file_name = raw_file_storage.upload_file(file.file, file.filename, file_uuid)

        logger.info(f"file_identifier: {stored_file_name}")
        query = insert(Files).values(
            original_filename=file.filename,
            uuid=file_uuid,
            s3_key=stored_file_name if isinstance(raw_file_storage, S3Storage) else None,
            local_path=stored_file_name if isinstance(raw_file_storage, LocalStorage) else None,
            uploader_id=None,
            upload_timestamp=datetime.now(),
            status=FileStatus.pending,
            file_type=file_extension,
            description=None
        )
        logger.info(f"Inserting file record: {file.filename}")
        logger.info(f"sql query: {query.compile()}")
        async with AsyncSessionLocal() as session:
            async with session.begin():
                result = await session.execute(query)
                file_id = result.inserted_primary_key[0]
        logger.info(f"File record inserted with id: {file_id}")

        logger.info(f"Processing file: {file.filename}")
        local_path = os.path.join(raw_file_storage.base_directory, stored_file_name)
        documents = processor.process(local_path)
        logger.info(f"Adding documents to vector store: {documents}")
        vector_store.add_documents(documents)
        logger.info(f"Documents added to vector store.")

        update_query = update(Files).where(Files.id == file_id).values(status=FileStatus.indexed)
        logger.info(f"Updating file status to indexed for file id: {file_id}")
        logger.info(f"sql query: {update_query.compile()}")
        async with AsyncSessionLocal() as session:
            async with session.begin():
                await session.execute(update_query)

        return {"status": "success", "uuid": file_uuid, "file_identifier": stored_file_name}
    except ValueError as e:
        logger.warning(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        if stored_file_name in locals():
            raw_file_storage.delete_file(stored_file_name)
            update_query = update(Files).where(Files.c.uuid == file_uuid).values(status=FileStatus.failed)
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    await session.execute(update_query)
            logger.info(f"File {stored_file_name} deleted.")
        raise HTTPException(status_code=500, detail="Error processing request")


@app.get("/api/files", summary="List files")
async def list_files():
    try:
        query = select(Files)
        async with AsyncSessionLocal() as session:
            async with session.begin():
                result = await session.execute(query)
                file_data = result.scalars().all()
                file_list = [
                    {
                        "id": f.id,
                        "original_filename": f.original_filename,
                        "uuid": f.uuid,
                        "s3_key": f.s3_key,
                        "local_path": f.local_path,
                        "uploader_id": f.uploader_id,
                        "status": f.status.value,
                        "upload_timestamp": f.upload_timestamp.isoformat(),
                        "file_type": f.file_type,
                        "description": f.description
                    }
                    for f in file_data
                ]
                logger.debug(f"Returning {file_list} files.")
                return {"files": file_list}
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Error processing request")


@app.get("/", summary="Root endpoint")
def read_root():
    """
    Root endpoint to verify that the API is running.
    """
    return {"message": "Welcome to the RAG FastAPI Application!"}