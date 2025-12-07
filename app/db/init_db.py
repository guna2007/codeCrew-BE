from sqlmodel import SQLModel

from app.db.session import engine
from app.models.user import User  # noqa: F401  (import so metadata sees User)


def init_db() -> None:
    # This will create all tables defined on SQLModel metadata (like User)
    SQLModel.metadata.create_all(bind=engine)
