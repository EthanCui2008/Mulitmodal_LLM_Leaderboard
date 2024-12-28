from lxml import html
import requests

def HTML_from_Xpath(url: str, xpath: str) -> str:
    """
    Input: Url, Xpath [NOT FULL XPATH]
    Output: HTML elements from xpath
    given a URL and a relevant proper Xpath it collects all elements from that URL
    """

    page = requests.get(url)

    tree = html.fromstring(page.content)

    element = tree.xpath(xpath)

    outer_html_elements = html.tostring(element[0], pretty_print=True).decode()

    return outer_html_elements

def get_ebay_description(html_content: str) -> dict:
    """
    Input: HTML_contents
    Output: Dictionary of ebay description in dictionary format
    given an html element content returns a properly formatted dictionary
    """
    tree = html.fromstring(html_content)
    rows = tree.xpath('//dl[@data-testid="ux-labels-values"]')

    item_specifics = {}

    for row in rows:

        key = row.xpath('.//dt//span[@class="ux-textspans"]/text()')

        value = row.xpath('.//dd//span[@class="ux-textspans"]/text()')

        if key and value:

            item_specifics[key[0].strip()] = value[0].strip()

    return item_specifics

def get_ebay_image_url(html_content: str) -> str:
    """
    Input: HTML_contents
    Output: Image Url 
    given an html element content returns an image url
    """
    tree = html.fromstring(html_content)

    image_url = tree.xpath('//img/@data-zoom-src')

    return image_url[0]