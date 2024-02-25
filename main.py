from db import DB
from user_crud import UserRepo

add_user = UserRepo().add

user_example = {
    "name": "Endy",
    "email": "eb_azul@email.co"
}

def main():
    user = add_user(user=user_example)
    print(user)

main()
