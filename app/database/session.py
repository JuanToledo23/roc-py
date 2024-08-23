from sqlalchemy.orm import sessionmaker

from app.database.engine import engine

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
