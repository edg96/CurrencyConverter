import shutil
import unittest
from unittest.mock import patch
import tempfile
import os
import tkinter as tk

import customtkinter as ctk

from src.currencyconverter.auxiliar import browse_folder, read_from_file_by_line


class TestAuxiliar(unittest.TestCase):
    """
    Unit tests for the Auxiliar module.
    """

    def setUp(self):
        """
        Set up a temporary directory for testing.
        """
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """
        Remove the temporary directory after testing.
        """
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_browse_folder(self):
        """
        Test the browse_folder function.

        This function should invoke the askdirectory method and set the result as the entry widget's content.
        """
        with patch('tkinter.filedialog.askdirectory', return_value='/mocked/folder/path'):
            master = tk.Tk()
            entry_widget = ctk.CTkEntry(master=master)
            browse_folder(entry_widget)
            self.assertEqual(entry_widget.get(), '/mocked/folder/path')

    def test_read_from_file_by_line(self):
        """
        Test the read_from_file_by_line function.

        This function should read lines from a file and return a list of lines.
        """
        temp_file_path = os.path.join(self.temp_dir, 'temp_file.txt')
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write("Line 1\nLine 2\nLine 3")

        lines = read_from_file_by_line(temp_file_path)
        expected_lines = ['Line 1', 'Line 2', 'Line 3']
        self.assertEqual(lines, expected_lines)

    def test_read_from_file_by_line_file_not_found(self):
        """
        Test the read_from_file_by_line function when the file is not found.

        This function should handle FileNotFoundError gracefully and print an error message.
        """
        non_existent_file_path = '/non_existent_file.txt'
        with patch('builtins.print') as mock_print:
            lines = read_from_file_by_line(non_existent_file_path)
            self.assertEqual(lines, [])
            mock_print.assert_called_with(f'File not found: {non_existent_file_path}')


if __name__ == '__main__':
    unittest.main()
