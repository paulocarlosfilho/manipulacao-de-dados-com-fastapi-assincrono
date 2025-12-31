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
    async with engine.begin() as conn:
        # Import models here to ensure they are registered with metadata
        from .models.post import post_table
        await conn.run_sync(metadata.create_all)
    _db_initialized = True
