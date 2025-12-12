from core.config import settings
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
DB_URL = settings.DATABASE_URL


async_engine = create_async_engine(
    url=DB_URL,
    echo=True,
)

async def init_db():
    import models
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all) 

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
async def get_db():
    async with async_session() as db:
        try:
            yield db
        finally:
            await db.close()