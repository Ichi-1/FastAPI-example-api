from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import env


SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{env.DB_USERNAME}:{env.DB_PASSWORD}'
    f'@{env.DB_HOSTNAME}:{env.DB_PORT}/{env.DB_NAME}'
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
