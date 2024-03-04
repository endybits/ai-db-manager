import json
import asyncio
from openai import OpenAI
from dotenv import load_dotenv

from utils.data_manager_functions import (
        add_user as create_user,
        get_all_users,
        get_user_by_id,
        update_user,
        delete_user
)
from models import User

load_dotenv() # Load environment variables from .env file

# api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

async def add_user_with_ai(user: dict):
    action = f"Adding user: {user}"
    print(action)
    result = await create_user(user)
    print(result)
    return result

async def list_users_with_ai():
    action = "Getting all users..."
    print(action)
    user_list = []
    result = await get_all_users()
    for user in result:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })
    return user_list

async def get_user_with_ai(user_id: int):
    action = f"Getting user with id {user_id}"
    print(action)
    user = await get_user_by_id(user_id)
    if isinstance(user, User):
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    return user

async def update_user_with_ai(user_id: int, user: dict):
    action = f"Updating user with id {user_id}"
    print(action)
    result = await update_user(user_id, user)
    print(result)
    return result

async def delete_user_with_ai(user_id: int):
    action = f"Deleting user with id {user_id}"
    print(action)
    result = await delete_user(user_id)
    print(result)
    return result

async def ai_DB_manager(user_question: str):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_user_with_ai",
                "description": "Create a user in the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "The name of the user"
                                },
                                "email": {
                                    "type": "string",
                                    "description": "The email of the user"
                                }
                            },
                            "required": ["name"]
                        },
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_users_with_ai",
                "description": "Get all users from the database",
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_user_with_ai",
                "description": "Get a user from the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The id of the user"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_user_with_ai",
                "description": "Update a user in the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The id of the user"
                        },
                        "user": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "The name of the user"
                                },
                                "email": {
                                    "type": "string",
                                    "description": "The email of the user"
                                }
                            }
                        }
                    },
                    "required": ["user_id", "user"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_user_with_ai",
                "description": "Delete a user from the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The id of the user"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
    ]
    messages = [
            {
                "role": "system",
                "content": "A great AI-driven assistant is here to help you with your database management needs. What would you like to do?" 
            },
            {
                "role": "user",
                "content": "User question: " + user_question
            }
        ]
    response =  client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        tools=tools
    )
    response_message = response.choices[0].message
    print("***************************")
    print("Response message: \n", response_message)
    print("***************************")
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "add_user_with_ai": add_user_with_ai,
            "list_users_with_ai": list_users_with_ai,
            "get_user_with_ai": get_user_with_ai,
            "update_user_with_ai": update_user_with_ai,
            "delete_user_with_ai": delete_user_with_ai
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            print("Tool call: \n", tool_call)
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = await function_to_call(**function_args)
            function_response = json.dumps(function_response)
            message_content = {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
            print("Message content: \n", message_content)
            messages.append(message_content)
            print("***************************")
            print("First response: \n", function_response)
            print("***************************")
            second_response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=messages,
            )
            
        return second_response.choices[0].message.content
    print("***************************")
    return response_message.content
