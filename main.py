from db import DB
from user_crud import UserRepo
from models import User
from utils import (
                    add_user,
                    get_all_users,
                    get_user_by_id,
                    update_user,
                    delete_user)


user_example = {
    "name": "Example_4",
    "email": "in_utils@email.co"
}
user_example_for_update = {
    #"name": "EndyB",
    "email": "updated@email.co"
}


def main():
    # Add user
    # user = add_user(user=user_example)
    
    # Get all users
    users = get_all_users()
    for user in users:
        print(user.id, user.name, user.email)
    
    # Update user
    user = update_user(2, user_example_for_update)
    if isinstance(user, User):
        print(user.id, user.name, user.email)
    else:
        print(user)

    # Get user by id
    user = get_user_by_id(2)
    if isinstance(user, User):
        print(user.id, user.name, user.email)
    else:
        print(user)

    # Delete user
    user = UserRepo().delete(2)
    print(user)

main()
