from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_engine(
    settings.db_url
)

Session = sessionmaker(
    bind = engine,
    expire_on_commit=False
)

