import asyncio

from utils.user_crud import UserRepo

async def add_user(user: dict):
    return await UserRepo().add(user)


async def get_all_users():
    return await UserRepo().fetch_all()


async def get_user_by_id(user_id: int):
    retrieved_user = await UserRepo().fetch_by_id(user_id)
    return retrieved_user

async def get_last_user_added(user_name: str):
    return await UserRepo().fetch_last_added(user_name)

async def update_user(user_id: int, user: dict):
    updated_data = await UserRepo().update(user_id, user)
    return updated_data

async def delete_user(user_id: int) -> str:
    return await UserRepo().delete(user_id)