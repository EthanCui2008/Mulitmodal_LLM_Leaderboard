import os
import utils
import json

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
load_dotenv(env_path)
client = OpenAI(api_key=os.getenv("open-ai_api_key"))

def normalize_data(input, function):
    tools = []

    func = {"type": "function",
                "function": {
                    "name": function["name"],
                    "description" :function["description"],
                    "parameters": function["parameters"]
                },
            }
    tools.append(func)

    completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "given this description in the form of a dictionary, fill out the relevant function call" + str(input),
                        }
                    ],
                }
            ],
            tools=tools
        )
    
    return str(completion.choices[0].message.tool_calls)