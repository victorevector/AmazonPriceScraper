import requests
from bs4 import BeautifulSoup

UPC2APC_URL = 'http://upctoasin.com/'
ASIN_VALID_LENGTH = 10
AMAZON_URL = 'http://amazon.com/gp/product/'

def pipeline(upc):
    return find_price(soupify( upc2asin(upc ) ) )

def upc2asin(upc):
    asin = requests.get(UPC2APC_URL + upc).content
    if len(asin) != ASIN_VALID_LENGTH: 
        return None 
    else:
        return {'upc': upc, 'asin': asin}

def soupify(kwargs):
    if kwargs is not None:
        asin = kwargs['asin']
        product = requests.get(AMAZON_URL + asin)
        kwargs['soup'] = BeautifulSoup(product.content)
        return kwargs
    else:
        return None

def find_price(kwargs):
    # The price is embedded in either of 2 <div> elements. This block makes sure to look through both...
    if kwargs is not None:
        soup = kwargs.pop('soup', None)
        price_html = soup.find(id='actualPriceValue') 
        if price_html is None:
            price_html = soup.find(id='priceblock_ourprice')
    else:
        return None
    try:
        kwargs['price'] = price_html.get_text()
        return kwargs
    except AttributeError:
        return None
