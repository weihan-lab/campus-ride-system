from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Connection string using asyncpg driver
HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "5432")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

# Note the change to +asyncpg
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

# SQLALCHEMY_DATABASE_URL = 'postgresql+asyncpg://postgres:Campusride%402626@db:5432/postgres'
# # Create Async Engine
# engine = create_async_engine(
#     SQLALCHEMY_DATABASE_URL,
#     echo=False,
#     future=True
# )

# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
