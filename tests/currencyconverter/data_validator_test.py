import unittest
from unittest.mock import patch
from src.currencyconverter.data_validator import DataValidator, InvalidLocationException


class TestDataValidator(unittest.TestCase):
    """
    Unit tests for the DataValidator class.
    """

    def setUp(self):
        """
        Set up a DataValidator instance for testing.
        """
        self.currency_widgets = []
        self.value_widgets = []
        self.data_validator = DataValidator(self.currency_widgets, self.value_widgets)

    @patch('src.currencyconverter.data_validator.browse_folder')
    def test_validate_and_save_to_excel_invalid_location(self, mock_browse_folder):
        """
        Test the validate_and_save_to_excel method with an invalid location.

        This test should ensure that the InvalidLocationException is raised when attempting to save to an invalid location.
        """
        mock_browse_folder.return_value = '/nonexistent/folder'

        with self.assertRaises(InvalidLocationException):
            self.data_validator.validate_and_save_to_excel()


if __name__ == '__main__':
    unittest.main()
