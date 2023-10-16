import os
import re
import traceback
from pathlib import Path

import customtkinter as ctk

from src.currencyconverter.excel_converter import ExcelConverter
from src.currencyconverter.auxiliar import browse_folder


class InvalidLocationException(Exception):
    """
    Custom exception class for invalid save location, raised when the provided save location
    is invalid or doesn't exist.
    """
    def __init__(self):
        super().__init__('Invalid save location')


class InvalidLengthException(Exception):
    """
    Custom exception class for invalid length, raised when the length of the provided name is
    greater than the allowed limit.
    """
    def __init__(self):
        super().__init__('Invalid length')


class InvalidNameException(Exception):
    """
    Custom exception class for an invalid name, raised when the provided name contains invalid
    characters.
    """
    def __init__(self):
        super().__init__('Invalid name')


class DataValidator(ctk.CTkToplevel):
    """
    The DataValidator class is responsible for providing a GUI interface for the user where the
    providing details must be checked and validated in order for the Windows operating system to
    save the file.

    Attributes:
        currency_widgets (list[ctk.CTkLabel]): A list of currency widgets from the main window.

        value_widgets (list[ctk.CTkFrame]): A list of value entries from the main window.
        currencies.

        self.title (str): The title of the application.

        self.geometry (str): The window size in height and width.

        self.resizable (bool, bool): A tuple of two booleans responsible for blocking the window to
        not be resizable both by height or width.

        self.configure(bg='#222629'): The background color of the window application.

        self.after(250, lambda: self.iconbitmap(os.path.join(Path(__file__).resolve().
        parent.parent.parent, 'resources', 'CurrencyConverter.ico'))): Sets the window icon to the
        specified image after 250 milliseconds (CustomTkinter has a bug where a delay should be
        placed in order for the icon to load and be dispalyed: can't provide the lowest delay acceptable).

    Note:
    - The DataValidator class also provide the option to save the data to a CSV file if the checks
    pass and the details are valid.
    """
    def __init__(self, currency_widgets, value_widgets):
        super().__init__()
        self.currency_widgets = currency_widgets
        self.value_widgets = value_widgets
        self.title(' Currency Converter')
        self.geometry('300x185')
        self.resizable(False, False)
        self.configure(bg='#222629')
        self.after(250, lambda: self.iconbitmap(os.path.join(Path(__file__).resolve().parent.parent.parent,
                                                             'resources', 'Save.ico')))

        self.save_location_entry = ctk.CTkEntry(master=self, placeholder_text='Insert the saving location',
                                                width=280, font=('Halvica', 14, 'bold'))
        self.excel_name_entry = ctk.CTkEntry(master=self, placeholder_text='Insert the name',
                                             width=280, font=('Halvica', 14, 'bold'))
        self.save_location_button = ctk.CTkButton(master=self, text='Browse folder', font=('Halvica', 14, 'bold'),
                                                  hover_color='#0034B3',
                                                  command=lambda: browse_folder(self.save_location_entry))
        self.confirm_saving_button = ctk.CTkButton(master=self, text='Save to Excel', fg_color='#00AF22',
                                                   font=('Halvica', 14, 'bold'), hover_color='#0034B3',
                                                   command=lambda: self.validate_and_save_to_excel())
        self.save_location_entry.grid(row=0, column=0, padx=(10, 0), pady=(15, 0))
        self.excel_name_entry.grid(row=1, column=0, padx=(10, 0), pady=(15, 0))
        self.save_location_button.grid(row=2, column=0, padx=(10, 0), pady=(15, 0), sticky='w')
        self.confirm_saving_button.grid(row=3, column=0, padx=(10, 0), pady=(15, 0), sticky='w')

    def validate_and_save_to_excel(self) -> None:
        """
        Validate the save location and name inputs.

        Saves currency conversion details to an Excel file if valid, otherwise raise custom
        exceptions (existence, name validity according to Windows File standards and file name length).
        """
        saving_location = self.save_location_entry.get()
        excel_name = self.excel_name_entry.get()

        try:
            # Validate saving_location
            if not os.path.exists(saving_location):
                raise InvalidLocationException()

            # Validate excel_name length
            if len(excel_name) > 31:
                raise InvalidLengthException()

            # Validate excel_name
            if re.search(r'[\\!/?:*\[\]]', excel_name):
                raise InvalidNameException()

            self.save_to_excel(saving_location, excel_name, self.currency_widgets, self.value_widgets)
        except (InvalidLengthException, InvalidNameException, FileNotFoundError) as e:
            traceback.print_exception()
            print(e)

    @staticmethod
    def save_to_excel(saving_location: str, excel_name: str, currency_widgets: list[ctk.CTkLabel],
                      value_widgets: list[ctk.CTkEntry]) -> None:
        """
        Save currency conversion details to an Excel file.

        Parameters:
            saving_location (str): The location where the Excel file should be saved.
            excel_name (str): The name of the Excel file.
            currency_widgets (list[ctk.CTkLabel]): List of custom tkinter label widgets representing
            currency names.
            value_widgets (list[ctk.CTkEntry]): List of custom tkinter entry widgets representing
            currency values.
        """
        ec = ExcelConverter(saving_location, excel_name, currency_widgets, value_widgets)
        ec.export_to_csv()
