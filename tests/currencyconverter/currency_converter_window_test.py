import unittest
from unittest.mock import MagicMock
from tkinter import Tk

from customtkinter import CTkEntry

from src.currencyconverter.currency_converter import CurrencyConvertor
from src.currencyconverter.currency_converter_window import CurrencyConverterWindow


class TestCurrencyConverterWindow(unittest.TestCase):
    """
    Unit tests for the CurrencyConverterWindow class.
    """

    def setUp(self):
        """
        Set up a CurrencyConvertorWindow instance for testing with USD as the currency reference.
        """
        self.root = Tk()
        self.root.withdraw()

        self.currency_converter = CurrencyConvertor('USD')

        self.currency_converter_window = CurrencyConverterWindow()
        self.currency_converter_window.root = self.root

    def tearDown(self):
        """
        Destroy the CurrencyConverterWindow after testing.
        """
        self.root.destroy()

    def test_split_value_currency(self):
        """
        Test the split_value_currency method.

        This method should split the value and currency in the entry widget when the 'Return' key is pressed.
        """
        event_mock = MagicMock()
        event_mock.keysym = 'Return'

        self.currency_converter_window.value_to_convert_entry.insert(0, '10 USD')

        self.currency_converter_window.split_value_currency(event_mock)

        self.assertEqual(self.currency_converter_window.value_to_convert_entry.get(), '10 USD')

    def test_reset_currency(self):
        """
        Test the reset_currency method.

        This method should reset the currency_for_reference attribute in the currency converter to 'USD'.
        """
        self.currency_converter_window.value_widgets = [
            CTkEntry(self.currency_converter_window), CTkEntry(self.currency_converter_window)
        ]

        self.currency_converter_window.reset_currency()

        self.assertEqual(self.currency_converter_window.currency_converter.currency_for_reference, 'USD')


if __name__ == '__main__':
    unittest.main()
