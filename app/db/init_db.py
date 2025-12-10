from sqlmodel import SQLModel

from app.db.session import engine
from app.models.user import User  # noqa: F401
from app.models.platform_account import PlatformAccount  # noqa: F401
from app.models.snapshot import PlatformSnapshot  # noqa: F401


def init_db() -> None:
    # This will create all tables defined on SQLModel metadata (User, PlatformAccount, PlatformSnapshot, etc.)
    SQLModel.metadata.create_all(bind=engine)
