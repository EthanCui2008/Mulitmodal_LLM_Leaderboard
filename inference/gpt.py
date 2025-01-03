import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
load_dotenv(env_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def inference_gpt(data):
    question_id = data.get("id")
    question_content = data.get("question", [[]])[0][0]["content"]
    function_details = data.get("function", [])[0]
    tools = [
        {
            "type": "function",
            "function": {
                "name": function_details["name"],
                "description" :function_details["description"],
                "parameters": function_details["parameters"]
            },
        }
    ]

    # Make the API call
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": question_content}],
        tools=tools,
    )

    # Extract and return the tool call result
    tool_calls = completion.choices[0].message.tool_calls
    return {
        "question_id": question_id,
        "tool_calls": tool_calls
    }

test ={
  "id": "simple_0",
  "question": [
    [
      {
        "role": "user",
        "content": "Find the area of a triangle with a base of 10 units and height of 5 units."
      }
    ]
  ],
  "function": [
    {
      "name": "calculate_triangle_area",
      "description": "Calculate the area of a triangle given its base and height.",
      "parameters": {
        "type": "object",
        "properties": {
          "base": {
            "type": "integer",
            "description": "The base of the triangle."
          },
          "height": {
            "type": "integer",
            "description": "The height of the triangle."
          },
          "unit": {
            "type": "string",
            "description": "The unit of measure (defaults to 'units' if not specified)"
          }
        },
        "required": [
          "base",
          "height"
        ]
      }
    }
  ]
}

print(inference_gpt(test))