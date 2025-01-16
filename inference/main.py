import json
import openai_handler

# Path to your JSONL file
jsonl_file = 'data/ebay-questions.jsonl'
handler = openai_handler.OpenAiHandler("gpt-4o-mini",0)

# Open the file and process each line
with open(jsonl_file, 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line.strip())
        print(handler.inference(data))