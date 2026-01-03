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

# Limpeza agressiva para evitar erros de copy-paste (psql, aspas, espaços)
DATABASE_URL = DATABASE_URL.strip().strip("'").strip('"')
if DATABASE_URL.startswith("psql "):
    DATABASE_URL = DATABASE_URL.replace("psql ", "", 1).strip().strip("'").strip('"')

# Tratamento para drivers assíncronos
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://") and "+asyncpg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Remove parâmetros de query que podem quebrar o parser do SQLAlchemy/asyncpg
if "?" in DATABASE_URL:
    base_url, query = DATABASE_URL.split("?", 1)
    # Mantemos apenas o que é essencial se necessário, ou limpamos tudo para usar connect_args
    DATABASE_URL = base_url

# Alerta de segurança/configuração
if "localhost" in DATABASE_URL and os.getenv("ENV") == "prod":
    logger.error("ERRO CRÍTICO: DATABASE_URL está usando 'localhost' em ambiente de PRODUÇÃO!")

# Configuração para o Render/Postgres Externo (SSL é obrigatório no Render)
connect_args = {}
if "render.com" in DATABASE_URL or os.getenv("ENV") == "prod":
    connect_args = {
        "ssl": "require",
        "server_settings": {
            "tcp_user_timeout": "10000",
        }
    }

engine = create_async_engine(
    DATABASE_URL, 
    echo=True, 
    poolclass=NullPool,
    connect_args=connect_args
)
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
