import os
import utils

from openai import OpenAI

from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
load_dotenv(env_path)

client = OpenAI(api_key=os.getenv("open-ai_api_key"))

def Open_AI_inference(data, model_id):

    question_content = data.get("question", [[]])[0][0]["content"]
    question_role = data.get("question", [[]])[0][0]["role"]

    image_path = data.get("question", [[]])[0][0]["image"]["file_path"]
    image_type = data.get("question", [[]])[0][0]["image"]["type"]

    base64_image = utils.encode_image(image_path)

    tools = []

    for function_details in data.get("function", []):
        func = {"type": "function",
                    "function": {
                        "name": function_details["name"],
                        "description" :function_details["description"],
                        "parameters": function_details["parameters"]
                    },
                }
        tools.append(func)
    
    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {
                "role": question_role,
                "content": [
                    {
                        "type": "text",
                        "text": question_content,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{image_type};base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        tools=tools
    )

    tool_calls = completion.choices[0].message.tool_calls

    return tool_calls