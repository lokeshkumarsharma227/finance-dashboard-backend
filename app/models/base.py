from sqlalchemy.orm import DeclarativeBase
# Base class that all SQLAlchemy models inherit from.
# When Base.metadata.create_all() runs, it finds every class
# that inherited Base and creates their tables in the database.

class Base(DeclarativeBase):
    pass