from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# O arquivo fica dentro do projeto, independente da pasta onde o comando é executado.
DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
DATA_DIRECTORY.mkdir(exist_ok=True)
DATABASE_URL = f"sqlite:///{DATA_DIRECTORY / 'barbearia.db'}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
