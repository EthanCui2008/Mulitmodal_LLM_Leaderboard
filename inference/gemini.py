import google.generativeai as genai
import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 

genai.configure(api_key=os.getenv("gemini_key"))

model_id = "gemini-1.5-pro-002"
product_classifier_system_instructions = """
Given a product image as input, extract relevant parameters and populate the arguments of a pre-defined function designed to process product information.
The model must understand the context of the image and accurately map visual features to function parameters.
"""
gemini_pro_002_FC = genai.GenerativeModel(model_name=model_id,
                                          system_instruction=product_classifier_system_instructions)


