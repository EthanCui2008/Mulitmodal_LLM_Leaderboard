import os
import json

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

#if I were a better coder I'd write this into a class, but because I'm expecting to only create about 50-200 samples I may as well write to the jsonl all at once, creating no real need to place the client object in a class instance

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
    tool_call = completion.choices[0].message.tool_calls[0]
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    return ([{"name":name,"args":args}])