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