from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from core.config import settings


# engine = create_engine(url=settings.DATABASE_URL)
engine = create_engine(url=settings.DATABASE_URL, pool_size=5, pool_recycle=3600)
# session_factory = sessionmaker(bind=engine)
# Session = scoped_session(session_factory)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
session = SessionLocal()


# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
# )


# # An instance of SessionLocal class will be the actual DB session
# # We will create a session for each request
# def get_session():
#     try:
#         session = SessionLocal()
#         # Base.metadata.create_all(engine)
#         yield session
#     except Exception:
#         session.rollback()
#     finally:
#         session.close()
#
