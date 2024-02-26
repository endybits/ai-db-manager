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
    ) -> str:
        user_obj = User(name=user['name'], email=user['email'])
        self.db.add(user_obj)
        self.db.commit()
        self.db.refresh(user_obj)
        return f"Added user {user_obj.name} with email {user_obj.email}"

    def fetch_by_id(self, user_id: int) -> User | str:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return f"User with id {user_id} not found"
        return user

    def fetch_all(self, skip: int = 0, limit: int = 10):
        return self.db.query(User).offset(skip).limit(limit).all()

    def delete(self, user_id: int) -> str:
        user = self.fetch_by_id(user_id)
        if not isinstance(user, User):
            return f"Coudn't delete user: User with id {user_id} not found"
        self.db.delete(user)
        self.db.commit()
        return f"Deleted user {user.name} with email {user.email}"

    def update(self, user_id: int, user: dict) -> str:
        user_obj = self.fetch_by_id(user_id)
        if not isinstance(user_obj, User):
            return f"Coudn't update user: User with id {user_id} not found"
        for key, value in user.items():
            setattr(user_obj, key, value)
        self.db.commit()
        self.db.refresh(user_obj)
        return f"Updated user {user_obj.name} with email {user_obj.email}"