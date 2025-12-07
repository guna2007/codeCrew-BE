from typing import Generator

from sqlmodel import Session, create_engine

from app.core.config import get_settings

settings = get_settings()

# echo=True prints SQL in console; useful while learning
engine = create_engine(settings.database_url, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
