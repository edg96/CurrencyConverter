import unittest
from doctest import master
import customtkinter as ctk
from src.currencyconverter.excel_converter import ExcelConverter


class TestExcelConverter(unittest.TestCase):
    """
    Unit tests for the ExcelConverter class.
    """

    def setUp(self):
        """
        Set up an ExcelConverter instance for testing.

        This method creates an instance of ExcelConverter with specified parameters for testing.
        """
        self.currency_widgets = [ctk.CTkLabel(master=master), ctk.CTkLabel(master=master)]
        self.value_widgets = [ctk.CTkEntry(master=master), ctk.CTkEntry(master=master)]
        self.excel_converter = ExcelConverter('/path/to/save', 'test_excel', self.currency_widgets, self.value_widgets)

    def test_saving_location_property(self):
        """
        Test the saving_location property.

        This test verifies that the saving_location property returns the expected value.
        """
        self.assertEqual(self.excel_converter.saving_location, '/path/to/save')

    def test_excel_name_property(self):
        """
        Test the excel_name property.

        This test verifies that the excel_name property returns the expected value.
        """
        self.assertEqual(self.excel_converter.excel_name, 'test_excel')


if __name__ == '__main__':
    unittest.main()
