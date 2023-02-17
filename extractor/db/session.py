from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from core.config import settings


engine = create_engine(
    url=settings.DATABASE_URL,
    pool_size=5,
    pool_recycle=3600,
    # echo=True,
    logging_name="sqlengine",
)
session = Session(bind=engine)


# session_factory = sessionmaker(bind=engine)
# Session = scoped_session(session_factory)

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
# )
# session = SessionLocal()

# # An instance of SessionLocal class will be the actual DB session
# # We will create a session for each request
# def get_session():
#     try:
#         session = SessionLocal()
#         yield session
#     except Exception:
#         session.rollback()
#     finally:
#         session.close()
#
