"""
Database initialization and setup.
"""

from sqlalchemy.orm import Session

from app.db.session import engine, Base
from app.models import user, candidate, interview, lookup


def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def create_initial_data(db: Session) -> None:
    """Create initial lookup data and admin user."""
    # This will be implemented when models are ready
    pass


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
