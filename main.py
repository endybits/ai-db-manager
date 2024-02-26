import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from db import DB
from user_crud import UserRepo
from models import User
from utils.data_manager_functions import (
        add_user,
        get_all_users,
        get_user_by_id,
        update_user,
        delete_user
)
from utils.ai_functions import ai_DB_manager

load_dotenv() # Load environment variables from .env file

# Create a new FastAPI instance
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# # Chatbot endpoint
@app.post("/ai-driven")
def ai_driven_chatbot(
    user_question: str
):
    try:
        ai_message = ai_DB_manager(user_question)
        return JSONResponse(content={"message": f"{ai_message}", "user_question": f"{user_question}"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)



## User CRUD endpoints
@app.get("/users")
def get_users():
    structured_users = []
    try:
        users = get_all_users()
        for user in users:
            structured_users.append({
                "id": user.id if user.id else None,
                "name": user.name if user.name else None,
                "email": user.email if user.email else None
            })
        return JSONResponse(content=structured_users, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.get("/user/{user_id}")
def get_one_user(user_id: int):
    try:
        user = get_user_by_id(user_id)
        if isinstance(user, User):
            return JSONResponse(content={
                "id": user.id if user.id else None,
                "name": user.name if user.name else None,
                "email": user.email if user.email else None
            }, status_code=200)
        else:
            return JSONResponse(content={"error": str(user)}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    

@app.post("/user")
def create_user(
    user: dict
):
    try:
        add_response = add_user(user)
        user_obj = UserRepo().fetch_last_added(user['name'])
        if user_obj:
            return JSONResponse(
                content= {
                    "message": f"{add_response}",
                    "data": [
                        {
                            "id": user_obj.id if user_obj.id else None,
                            "name": user_obj.name if user_obj.name else None,
                            "email": user_obj.email if user_obj.email else None
                        }
                    ]
                },
                status_code=201)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


@app.put("/user/{user_id}")
def update_one_user(
    user_id: int,
    user_data: dict
):
    try:
        serialized_user_data = json.dumps(user_data)
        if not user_data or len(user_data) == 0:
            raise Exception("No data to update")
        user_updated_message = update_user(user_id, json.loads(serialized_user_data))
        return JSONResponse(content={"message": user_updated_message}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


@app.delete("/user/{user_id}")
def delete_one_user(user_id: int):
    try:
        user_deleted_message = delete_user(user_id)
        return JSONResponse(content={"message": user_deleted_message}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)