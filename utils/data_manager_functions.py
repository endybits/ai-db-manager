from user_crud import UserRepo

def add_user(user: dict):
    return UserRepo().add(user)


def get_all_users():
    return UserRepo().fetch_all()


def get_user_by_id(user_id: int):
    retrived_user = UserRepo().fetch_by_id(user_id)
    return retrived_user


def update_user(user_id: int, user: dict):
    return UserRepo().update(user_id, user)

def delete_user(user_id: int) -> str:
    return UserRepo().delete(user_id)