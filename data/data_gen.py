import json
import os

jsonl_file_path = 'data/test-questions.jsonl'

# Ensure the directory exists (handles cases where the file is in a subdirectory)
directory = os.path.dirname(jsonl_file_path)
if directory:
    os.makedirs(directory, exist_ok=True)

with open('data\links.json', 'r') as file:
    links = json.load(file)
# List of image URLs to replace in the content
image_urls = links["test_links"]

# Base template dictionary
base_dict = {
    "id": "live_simple_0-0-0",
    "question": [
        [
            {
                "role": "user",
                "content": [
                    "Can you retrieve items that are blue and made of cotton, with a striped design?",
                    "https://images.example.com/products/blue-cotton-striped-shirt.jpg"
                ]
            }
        ]
    ],
    "function": [
        {
            "name": "get_color_design_material",
            "description": "Retrieve details based on specified color, design options, and material type.",
            "parameters": {
                "type": "dict",
                "required": [
                    "color",
                    "material"
                ],
                "properties": {
                    "color": {
                        "type": "string",
                        "description": "The color to filter the items. This parameter is required."
                    },
                    "material": {
                        "type": "string",
                        "description": "The material type to filter the items. This parameter is required."
                    },
                    "design": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "A list of design options to consider while retrieving details.",
                        "default": []
                    }
                }
            }
        }
    ]
}

# Function to increment the ID
def increment_id(current_id, increment=1):
    """
    Increments the last numerical segment of the ID.

    Parameters:
        current_id (str): The current ID string.
        increment (int): The amount to increment.

    Returns:
        str: The incremented ID string.
    """
    parts = current_id.split('-')
    # Assume the last part is the incrementing number
    last_num = int(parts[-1])
    new_num = last_num + increment
    parts[-1] = str(new_num)
    return '-'.join(parts)

# Open the JSONL file once in append mode
with open(jsonl_file_path, 'a', encoding='utf-8') as file:
    current_id = base_dict["id"]
    
    for idx, url in enumerate(image_urls):
        # Create a deep copy of the base dictionary to avoid modifying the original
        new_dict = json.loads(json.dumps(base_dict))
        
        # Increment the ID
        new_id = increment_id(current_id)
        new_dict["id"] = new_id
        
        # Update the content with the new URL
        new_dict["question"][0][0]["content"][1] = url
        
        # Optionally, update the text in the content if needed
        # For example, you can modify the query based on the URL or other parameters
        
        # Serialize the dictionary to a JSON-formatted string
        json_line = json.dumps(new_dict)
        
        # Write the JSON string followed by a newline character
        file.write(json_line + '\n')
        
        print(f"Appended ID: {new_id} with URL: {url}")
        
        # Update current_id for the next iteration
        current_id = new_id

print(f"\nSuccessfully appended {len(image_urls)} dictionaries to {jsonl_file_path}.")
