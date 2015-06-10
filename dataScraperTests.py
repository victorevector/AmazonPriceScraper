import responses
import unittest
from dataScraper import UPC2APC_URL, AMAZON_URL, upc2asin, soupify, find_price, pipeline
import requests
from bs4 import BeautifulSoup

def load_mockresponse(asin):
    filename = '{}.txt'.format(asin )
    with open(filename, 'r') as foo:
        mockresponse = foo.read()
    return mockresponse

Proper_UPC = '885370702903' #XBOX
Improper_UPC = '322'
Proper_ASIN = 'B00CMQTVUA'
Improper_ASIN = None
Expected_Price = '$424.99'
Mock_Response = load_mockresponse(Proper_ASIN)
Mock_Soup = BeautifulSoup( Mock_Response )

class TestIndividualFunctions(unittest.TestCase):
    """
    Test each individual function that makes up the dataScraper
    """

    @responses.activate
    def test_upc2asin_returns_proper_asin_and_upc(self):
        responses.add( responses.GET, UPC2APC_URL + Proper_UPC, body= Proper_ASIN )
        function_response = upc2asin(Proper_UPC )
        expected_response = {'upc': Proper_UPC, 'asin': Proper_ASIN}

        self.assertEqual( function_response, expected_response )

    @responses.activate
    def test_upc2asin_returns_none(self):
        responses.add( responses.GET, UPC2APC_URL + Improper_UPC, body= Improper_ASIN )
        function_response = upc2asin(Improper_UPC)
        expected_response = None

        self.assertEqual( function_response, expected_response)

    @responses.activate
    def test_soupify_returns_proper_soup_object(self):
        responses.add( responses.GET, AMAZON_URL + Proper_ASIN, body=Mock_Response )
        kwargs = {'upc': Proper_UPC, 'asin': Proper_ASIN}
        function_response = soupify(kwargs)

        self.assertEqual( function_response['soup'], BeautifulSoup(Mock_Response) )

    def test_soupify_returns_none(self):
        kwargs = None
        test_response = soupify(kwargs)

        self.assertEqual( test_response, None )

    def test_find_price_returns_proper_price(self):
        kwargs = {'upc': Proper_UPC, 'asin': Improper_ASIN, 'soup': Mock_Soup}
        function_response = find_price(kwargs)
        self.assertEqual( function_response['price'], Expected_Price )

    def test_find_price_returns_None(self):
        kwargs = None
        function_response = find_price(kwargs)
        self.assertEqual( function_response, None)

    @responses.activate
    def test_pipeline_returns_proper_price(self):
        responses.add( responses.GET, UPC2APC_URL + Proper_UPC, body= Proper_ASIN ) #Hooks upc2asin
        responses.add( responses.GET, AMAZON_URL + Proper_ASIN, body=Mock_Response ) #Hooks soupify
        function_response = pipeline(Proper_UPC)
        self.assertEqual( function_response['price'], Expected_Price )

    @responses.activate
    def test_pipeline_breaks_at_upc2apc(self):
        """
        upc2apc pushes an improper ASIN through the pipeline
        """
        responses.add( responses.GET, UPC2APC_URL + Proper_UPC, body= Improper_ASIN ) #Hooks upc2asin

        self.assertEqual( pipeline(Proper_UPC), None )

    @responses.activate
    def test_pipeline_breaks_at_soupify(self):
        """
        soupify pushes through improper web content through the pipeline
        """
        responses.add( responses.GET, UPC2APC_URL + Proper_UPC, body= Proper_ASIN ) #Hooks upc2asin
        responses.add( responses.GET, AMAZON_URL + Proper_ASIN, body=None ) #Hooks soupify

        self.assertEqual( pipeline(Proper_UPC), None )


if __name__ == '__main__':
    unittest.main()