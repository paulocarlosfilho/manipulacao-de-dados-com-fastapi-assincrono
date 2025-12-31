import os
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/blog_db")

engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

metadata = sa.MetaData()

_db_initialized = False

async def init_db():
    global _db_initialized
    if _db_initialized:
        return
    
    # Import models here to ensure they are registered with metadata
    from .models.post import post_table
    
    try:
        async with engine.begin() as conn:
            print("Initializing database...")
            # Em ambiente de teste, podemos querer recriar as tabelas
            if os.getenv("ENV") == "test":
                print("Test environment detected. Dropping tables...")
                await conn.run_sync(metadata.drop_all)
            
            await conn.run_sync(metadata.create_all)
            print("Database initialized successfully.")
        _db_initialized = True
    except Exception as e:
        print(f"Error initializing database: {e}")
        # Não marcamos como inicializado para tentar novamente se necessário
        raise e
