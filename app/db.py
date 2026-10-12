"""Storage configuration. Passwords must never be logged."""
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

def get_engine_url() -> URL:
    explicit = os.getenv('DATABASE_URL')
    if explicit:
        return make_url(explicit)
    return URL.create('postgresql+psycopg',
        username=os.getenv('DB_USER', 'pe_planning'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '5432')),
        database=os.getenv('DB_NAME', 'pe_planning'))

engine = create_engine(get_engine_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def get_db():
    with SessionLocal() as session:
        yield session
