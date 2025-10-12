from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url
from app.core.config import settings

url = make_url(settings.DATABASE_URL)
engine_kwargs = {"pool_pre_ping": True}
if url.get_backend_name() == "sqlite":
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
