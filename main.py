from db import DB
from user_crud import UserRepo

add_user = UserRepo().add

user_example = {
    "name": "Endy",
    "email": "eb_updated_azul@email.co"
}

def get_all_users():
    return UserRepo().fetch_all()

def main():
    # Add user
    # user = add_user(user=user_example)
    
    # Get all users
    users = get_all_users()
    for user in users:
        print(user.id, user.name, user.email)
    
    # Update user
    user = UserRepo().update(2, user_example)

    # Get user by id
    user = UserRepo().fetch_by_id(2)
    print(user.id, user.name, user.email)
    
    # Delete user
    user = UserRepo().delete(2)
    print(user)

main()
