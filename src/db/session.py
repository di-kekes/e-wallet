from sqlalchemy.orm import sessionmaker
from src.config import get_settings
from sqlalchemy import create_engine

settings = get_settings()
engine = create_engine(
    url=settings.DATABASE_URL,
    future=True,
)

SessionFactory = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
