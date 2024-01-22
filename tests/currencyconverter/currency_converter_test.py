import unittest
from unittest.mock import patch, MagicMock

from src.currencyconverter.currency_converter import CurrencyConvertor


class TestCurrencyConvertor(unittest.TestCase):
    """
    Unit tests for the CurrencyConvertor class.
    """

    def setUp(self):
        """
        Set up a CurrencyConvertor instance for testing with USD as the currency reference.
        """
        self.currency_converter = CurrencyConvertor(currency_for_reference='USD')

    @patch('src.currencyconverter.currency_converter.requests.get')
    def test_fetch_exchange_rates_failure(self, mock_requests_get):
        """
        Test the _fetch_exchange_rates method when a web request fails.

        This method should handle exceptions raised during web requests and set exchange_rates to an empty dictionary.
        """
        mock_requests_get.side_effect = Exception('Mocked exception')

        self.currency_converter._fetch_exchange_rates()

        self.assertEqual(self.currency_converter.exchange_rates, {})


if __name__ == '__main__':
    unittest.main()
