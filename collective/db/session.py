from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


engine = create_engine(
    url=settings.DATABASE_URL,
    pool_size=5,
    pool_recycle=3600,
    # echo=True,
    logging_name="sqlengine",
)
Session = sessionmaker(bind=engine)
