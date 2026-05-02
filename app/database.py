from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from core import settings
from models import User

DATABASEURL = settings.DATABASE_URL

db_engine = create_engine(DATABASEURL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
