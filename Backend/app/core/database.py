from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.core.config import settings

# Create Async Engine
# echo=True will log all SQL queries (useful for development)
engine = create_async_engine(settings.database_url, echo=False)

# Session factory for async sessions
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    """
    Initialize the database, creating all tables defined in SQLModel.
    """
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    """
    Dependency to get an async database session for API routes.
    """
    async with async_session_factory() as session:
        yield session
