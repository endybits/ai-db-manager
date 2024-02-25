from sqlalchemy.orm import Session

from db import DB
from models import User



class UserRepo:
    def __init__(self):
        self.db = DB().session_factory

    def add(
        self,
        user: dict = {
            'name': str,
            'email': str,
        }
    ):
        user_obj = User(name=user['name'], email=user['email'])
        self.db.add(user_obj)
        self.db.commit()
        self.db.refresh(user_obj)
        return f"Added user {user_obj.name} with email {user_obj.email}"

    def fetch_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def fetch_all(self, skip: int = 0, limit: int = 10):
        return self.db.query(User).offset(skip).limit(limit).all()

    def delete(self, user_id: int):
        user = self.fetch_by_id(user_id)
        self.db.delete(user)
        self.db.commit()
        return f"Deleted user {user.name} with email {user.email}"

    def update(self, user_id: int, user: dict):
        user_obj = self.fetch_by_id(user_id)
        user_obj.name = user['name'] if user['name'] else user.name
        user_obj.email = user['email'] if user['email'] else user.email
        self.db.commit()
        self.db.refresh(user_obj)
        return f"Updated user {user_obj.name} with email {user_obj.email}"