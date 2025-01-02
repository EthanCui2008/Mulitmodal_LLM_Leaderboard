import json
import os
from ebay import ebay_scraper as scraper
from ebay import ebay_normalizer as normalizer

description_Xpath = '//*[@id="viTabs_0_is"]/div'
image_Xpath = '//*[@id="PicturePanel"]/div[1]/div/div[1]/div[1]/div[2]/div[4]/div[1]/img'

with open('data/ebay/links.json', 'r') as file:
    links = json.load(file)
    test_links = links["test_links"]

with open('data/ebay/function_calls.json', 'r') as file:
    functions = json.load(file)
    
with open('data/ebay-questions.jsonl', 'a', encoding='utf-8') as questions, \
     open('data/ebay-groundtruth.jsonl', 'a', encoding='utf-8') as groundtruth:
    
    for link in test_links:
        item_specifics = scraper.get_ebay_description(scraper.HTML_from_Xpath(link, description_Xpath))
        image_url = scraper.get_ebay_image_url(scraper.HTML_from_Xpath(link, image_Xpath))

        
        