from eval import eval
from inference import gemini
from inference import openai_handler

import json

def main():
    client = openai_handler.OpenAiHandler("gpt-4o",0)
    ground_truth_path = 'data/ebay-groundtruth.jsonl'
    questions_path = 'data/ebay-questions.jsonl'
    with open(questions_path, 'r') as questions_file, open(ground_truth_path, 'r') as groundtruth_file:
        for question_line, ground_truth_line in zip(questions_file, groundtruth_file):
            ground_truth_data = json.loads(ground_truth_line)
            question_data = json.loads(question_line)
            raw_model_output = client.inference(question_data)
            model_data = client.post_process(raw_model_output)
            eval_model = model_data
            eval_ground = [ground_truth_data["ground_truth"][0]]
            print(eval.match(eval_ground, eval_model))

if __name__ == "__main__":
  main()