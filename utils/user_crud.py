import asyncio

from sqlalchemy import desc
from sqlalchemy.orm import Session

from db import DB
from models import User



class UserRepo:
    def __init__(self):
        self.db = DB().session_factory

    # Create
    async def add(
        self,
        user: dict = {
            'name': str,
            'email': str,
        }
    ) -> str:
        if not user.get('name'):
            raise Exception("Name is a required field")
        user_obj = User(
            name=user['name'],
            email=user['email'] if user.get('email') else None)
        self.db.add(user_obj)
        await asyncio.sleep(0)
        self.db.commit()
        self.db.refresh(user_obj)
        return f"Added user {user_obj.name} with email {user_obj.email}"

    # Read
    
    async def fetch_by_id(self, user_id: int) -> User | str:
        print("Is the error here? fetch_by_id")
        target_user = self.db.query(User).filter(User.id == user_id).first()
        print("Noooooo")
        await asyncio.sleep(0)
        if not target_user:
            return f"User with id {user_id} not found"
        return target_user

    async def fetch_all(self, skip: int = 0, limit: int = 10):
        user_list = self.db.query(User).offset(skip).limit(limit).all()
        await asyncio.sleep(0)
        return user_list

    async def fetch_last_added(self, user_name: str) -> User:
        last_user = self.db.query(User).filter(User.name == user_name).order_by(desc(User.id)).first()
        await asyncio.sleep(0)
        return last_user

    # Update
    async def update(self, user_id: int, user: dict) -> str:
        user_obj = await self.fetch_by_id(user_id)
        
        if not isinstance(user_obj, User):
            raise Exception(f"Couldn't update user: User with id {user_id} doesn't exist")
        for key, value in user.items():
            setattr(user_obj, key, value)
        self.db.commit()
        self.db.refresh(user_obj)
        await asyncio.sleep(0)
        return f"Updated user {user_obj.name} with email {user_obj.email}"

    # Delete
    async def delete(self, user_id: int) -> str:
        user = self.fetch_by_id(user_id)
        if not isinstance(user, User):
            raise Exception(f"Coudn't delete user: User with id {user_id} doesn't exist")
        self.db.delete(user)
        await asyncio.sleep(0)
        self.db.commit()
        return f"Deleted user {user.name} with email {user.email}"
