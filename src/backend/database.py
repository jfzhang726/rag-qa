# backend/database.py

import os 
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import logging
logger = logging.getLogger(__name__)


Base = declarative_base()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./rag_app.db")



# Create the asynchronous SQLAlchemy engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production to disable SQL query logging
    # connect_args={"check_same_thread": False}  # Required for SQLite
)
# Create a configured "Session" class for async operations
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)




# Metadata instance for table definitions
# metadata = MetaData()

async def init_db():
    logger.info("Initializing database.")
    # Initialize the database by creating all tables defined in the metadata
    # This function is called by the FastAPI event handler on startup
    import backend.models  # Import all models to ensure they are registered with metadata
    

    logger.info(f"Number of tables before creation: {len(Base.metadata.tables)}")
    

    async with engine.begin() as conn:
        # Create all tables
        logger.info("Creating tables.")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Tables created.")
        # optionally, you can drop all tables first in development
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
    logger.info(f"Number of tables after creation: {len(Base.metadata.tables)}")