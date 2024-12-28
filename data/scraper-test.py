import ebay_scraper as scraper
import json

with open('data\links.json', 'r') as file:
    links = json.load(file)

initial_teapot_link = links["test_links"][0]

description_Xpath = '//*[@id="viTabs_0_is"]/div'
image_Xpath = '//*[@id="PicturePanel"]/div[1]/div/div[1]/div[1]/div[2]/div[4]/div[1]/img'

item_specifics = scraper.get_ebay_description(scraper.HTML_from_Xpath(initial_teapot_link, description_Xpath))

image_url = scraper.get_ebay_image_url(scraper.HTML_from_Xpath(initial_teapot_link, image_Xpath))

print(image_url, item_specifics)