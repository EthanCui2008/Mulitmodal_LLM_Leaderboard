import os
import utils
import json

from base_handler import InferenceHandler
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv

class OpenAiHandler(InferenceHandler):
    def __init__(self, model_name, temperature) -> None:
        
        """
        inits the inference handler with the model name and creates an OpenAI client
        Args:
        model_name: The name of the OpenAI model
        Returns:
        nothing
        """

        super().__init__(model_name, temperature)

        env_path = find_dotenv()
        load_dotenv(env_path)
        self.client = OpenAI(api_key=os.getenv("open-ai_api_key"))

    def inference(self, input_data):

        question_content = input_data.get("question", [[]])[0][0]["content"]
        question_role = input_data.get("question", [[]])[0][0]["role"]

        image_path = input_data.get("question", [[]])[0][0]["image"]["file_path"]
        image_type = input_data.get("question", [[]])[0][0]["image"]["type"]

        base64_image = utils.encode_image(image_path)

        tools = []

        for function_details in input_data.get("function", []):
            func = {"type": "function",
                        "function": {
                            "name": function_details["name"],
                            "description" :function_details["description"],
                            "parameters": function_details["parameters"]
                        },
                    }
            tools.append(func)
        
        completion = self.client.chat.completions.create(
            model=self.model_name,
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
            temperature = self.temperature,
            tools=tools
        )

        tool_calls = completion.choices[0].message.tool_calls

        return tool_calls
    def post_process(model_output):
        normalized_data = 0
        return normalized_data
