import json
import os
from ebay import ebay_scraper as scraper
from ebay import ebay_normalizer as normalizer
import utils
# These are subject to change and this whole project is prone to breaking due to heavy reliance on Ebay web elements
description_Xpath = '//*[@id="viTabs_0_is"]/div'
image_Xpath = '//*[@id="PicturePanel"]/div[1]/div/div[1]/div[1]/div[2]/div[4]/div[1]/img'

mute = False

# Opens up relevant links 
with open('data/ebay/links.json', 'r') as file:
    links = json.load(file)
    test_links = links["test_links"]

# Opens up all functoin calls
with open('data/ebay/function_calls.json', 'r') as file:
    function_calls = json.load(file)

# Prepares to write to relevant jsonls
with open('data/ebay-questions.jsonl', 'a', encoding='utf-8') as questions_file, \
     open('data/ebay-groundtruth.jsonl', 'a', encoding='utf-8') as groundtruth_file:
    
    # Data for question names
    question_id = "ebay-question-"
    question_num = 0
    for link in test_links:
        try:
            # Pulls data from Ebay using scraper
            item_specifics_HTML = scraper.HTML_from_Xpath(link, description_Xpath)
            item_specifics = scraper.get_ebay_description(item_specifics_HTML)
            image_url_HTML = scraper.HTML_from_Xpath(link, image_Xpath)
            image_url = scraper.get_ebay_image_url(image_url_HTML)
            # Downloads image and returns relevant info
            
            image_type, image_path = utils.get_image(image_url,"data/images",(question_id+str(question_num)))

        except:
            if not mute:
                print("Webscraping error on this link: " + link)
            continue

        for function_id in function_calls:
            function_call = function_calls[function_id]["function"]
            function_call_question = function_calls[function_id]["question"]
            id = (question_id+str(question_num))
            # Normalizes data to create groundtruth for eval
            groundtruth = normalizer.normalize_data(item_specifics,function_call)

            # Writes groundtruth
            groundtruth_write = {"id":id,
                                 "ground_truth":groundtruth}
            groundtruth_file.write(json.dumps(groundtruth_write) + '\n')

            # Builds question
            question = [[{"role":"user",
                          "content":function_call_question,
                          "image":{
                              "file_path":image_path,
                              "type":image_type
                          }}]]

            # Writes question
            question_write = {"id":id,
                              "question":question,
                              "function":[function_call]}
            questions_file.write(json.dumps(question_write) + '\n')
            if not mute:
                print("Question Succesfully created with ID: " + id)
            question_num += 1