from lxml import html
import requests

class ScraperError(Exception):
    """Custom exception for scraper errors."""
    pass

def HTML_from_Xpath(url: str, xpath: str) -> str:
    """
    Input: Url, Xpath [NOT FULL XPATH]
    Output: HTML elements from xpath
    given a URL and a relevant proper Xpath it collects all elements from that URL
    """
    try:
        page = requests.get(url, timeout=10)
        page.raise_for_status() 
    except requests.RequestException as e:
        raise ScraperError(f"Failed to fetch URL: {url}. Error: {e}")
    
    try:
        tree = html.fromstring(page.content)
        element = tree.xpath(xpath)
        if not element:
            raise ScraperError(f"No elements found for XPath: {xpath} on URL: {url}.")
        
        outer_html_elements = html.tostring(element[0], pretty_print=True).decode()
        return outer_html_elements
    except Exception as e:
        raise ScraperError(f"Error processing XPath: {xpath} on URL: {url}. Error: {e}")

def get_ebay_description(html_content: str) -> dict:
    """
    Input: HTML_contents
    Output: Dictionary of ebay description in dictionary format
    given an html element content returns a properly formatted dictionary
    """
    try:
        tree = html.fromstring(html_content)
        rows = tree.xpath('//dl[@data-testid="ux-labels-values"]')
        if not rows:
            raise ScraperError("No item specifics found in the HTML content.")
        
        item_specifics = {}
        for row in rows:
            key = row.xpath('.//dt//span[@class="ux-textspans"]/text()')
            value = row.xpath('.//dd//span[@class="ux-textspans"]/text()')
            if key and value:
                item_specifics[key[0].strip()] = value[0].strip()
        
        if not item_specifics:
            raise ScraperError("Failed to parse item specifics into a dictionary.")
        
        return item_specifics
    except Exception as e:
        raise ScraperError(f"Error extracting eBay description. Error: {e}")

def get_ebay_image_url(html_content: str) -> str:
    """
    Input: HTML_contents
    Output: Image Url 
    given an html element content returns an image url
    """
    try:
        tree = html.fromstring(html_content)
        image_url = tree.xpath('//img/@data-zoom-src')
        if not image_url:
            raise ScraperError("No image URL found in the HTML content.")
        
        return image_url[0]
    except Exception as e:
        raise ScraperError(f"Error extracting eBay image URL. Error: {e}")
