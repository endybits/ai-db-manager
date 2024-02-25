from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String

class Base(DeclarativeBase):
    pass

# Path: models.py

class User(Base):
    __tablename__ = "user_account"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50), unique=True, nullable=True)

    def __repr__(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }