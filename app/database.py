import os
import logging
import sqlalchemy as sa

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
            logger.info("Initializing database...")
            # Em ambiente de teste, podemos querer recriar as tabelas
            if os.getenv("ENV") == "test":
                logger.info("Test environment detected. Dropping tables...")
                # Segurança extra: garante que estamos no banco de teste ou localhost
                if "blog_db" in DATABASE_URL or "localhost" in DATABASE_URL:
                    await conn.run_sync(metadata.drop_all)
                else:
                    logger.warning("Skipping drop_all for safety: DATABASE_URL doesn't look like a test DB.")
            
            await conn.run_sync(metadata.create_all)
            logger.info("Database initialized successfully.")
        _db_initialized = True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        # Não marcamos como inicializado para tentar novamente se necessário
        raise e
