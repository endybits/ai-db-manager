import json
import os
from openai import OpenAI
from dotenv import load_dotenv

from utils.data_manager_functions import (
        add_user as create_user,
        get_all_users
)
from models import User

load_dotenv() # Load environment variables from .env file

# api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

def add_user(user: dict):
    action = f"Adding user: {user}"
    print(action)
    result = create_user(user)
    print(result)
    return result

def list_users():
    action = "Getting all users..."
    print(action)
    user_list = []
    result = get_all_users()
    for user in result:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })
    return user_list


def ai_DB_manager(user_question: str):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_user",
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
                "name": "list_users",
                "description": "Get all users from the database",
            }
        },
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
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        tools=tools
    )
    
    response_message = response.choices[0].message
    
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "add_user": add_user,
            "list_users": list_users
        }
        messages.append(response_message)

        for tool_call in tool_calls:
            print("Tool call: \n", tool_call)
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            function_response = json.dumps(function_response)
            message_content = {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
            print("Message content: \n", message_content)
            messages.append(message_content)
            
            second_response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=messages,
            )
        return second_response.choices[0].message.content
    return response_message.content
