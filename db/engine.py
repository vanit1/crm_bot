from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def async_engine_(url : str) -> AsyncEngine:
    return create_async_engine(url)

async def process_schemas(engine : AsyncEngine, metadata):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

def get_session_maker(engine : AsyncEngine):
    return sessionmaker(engine, class_=AsyncSession)