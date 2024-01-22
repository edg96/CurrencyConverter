import os
import re
from pathlib import Path

import customtkinter as ctk

from src.currencyconverter.currency_converter import CurrencyConvertor
from src.currencyconverter.data_validator import DataValidator


"""
================== Application description ==================

The application allows users to convert currency values and save the converted data to an Excel file.

Classes (all defined externally):
    - CurrencyConverterWindow: The main application window, responsible for currency conversion and 
    display.
    - ExcelDetails: A class responsible for saving currency details to an Excel file.

Usage:
    - Instantiate the CurrencyConverterWindow class to launch the currency conversion application.

Note:
    - This script uses the external library 'customtkinter' for creating a GUI interface.
"""


class CurrencyConverterWindow(ctk.CTk):
    """
    The CurrencyConverterWindow is the main window of the application, containing the currency details
    and the options of saving the currency data (the results) or clearing the data (which act as a
    reset where USD is the currency reference).

    Attributes:
        self.title (str): The title of the application.

        self.geometry (str): The window size in height and width.

        self.resizable (bool, bool): A tuple of two booleans responsible for blocking the window to
        not be resizable both by height or width.

        self.configure(bg='#222629'): The background color of the window application.

        self.radio_current_option (int): An integer representing the current selected radio option.

        self.dropdown_current_option (str): A string representing the current selected dropdown option.

        self.after(250, lambda: self.iconbitmap(os.path.join(Path(__file__).resolve().
        parent.parent.parent, 'resources', 'CurrencyConverter.ico'))): Sets the window icon to the
        specified image after 250 milliseconds (CustomTkinter has a bug where a delay should be
        placed in order for the icon to load and be displayed: can't provide the lowest delay acceptable).

        self.currency_converter (CurrencyConvertor): An instance of the CurrencyConvertor class with
        'USD' as the initial currency reference.

        self.toplevel_window (ExcelDetails or None): A reference to the ExcelDetails window for saving
        currency details or None if it doesn't exist.

        self.index (int): An index used for tracking continents.

        self.currency_widgets (list[ctk.CTkLabel]): A list of currency label widgets.

        self.value_widgets (list[ctk.CTkEntry]): A list of value entry widgets.

    Notes:
        - An initial instance of CurrencyConverter should be provided with a specified currency
        reference (chose USD for convince and international usage)
    """
    def __init__(self):
        super().__init__()
        self.title(' Currency Converter')
        self.geometry('1014x660')
        self.resizable(False, False)
        self.configure(bg='#222629')
        self.after(250, lambda: self.iconbitmap(os.path.join(Path(__file__).resolve().parent.parent.parent,
                   'resources', 'icons', 'CurrencyConverter.ico')))
        self.currency_converter = CurrencyConvertor('USD')
        self.radio_current_option = 0
        self.dropdown_current_option = ''
        self.toplevel_window = None
        self.index = 0
        self.currency_widgets = []
        self.value_widgets = []

        self.currency_converter.fetch_all_details()

        self.value_to_convert_entry = ctk.CTkEntry(master=self, placeholder_text='Insert value')

        for index, continent in enumerate(self.currency_converter.continents):
            self.continent_frame = ctk.CTkFrame(master=self, width=172, height=580, corner_radius=20,
                                                border_width=1, border_color='#474B4F')
            self.continent_frame.grid_propagate(False)
            self.continent_frame.grid(row=0, column=index, padx=15, pady=(13, 0))

            currency_of_continent = self.currency_converter.currency_per_continent[continent]
            row_index = 0
            column_index = 0

            for currency_name, currency_value in currency_of_continent.items():
                currency = ctk.CTkLabel(self.continent_frame, text=currency_name)
                value = ctk.CTkEntry(self.continent_frame, width=100)

                currency.grid(row=row_index, column=column_index, padx=(10, 5), pady=(5, 5))
                value.grid(row=row_index, column=column_index+1, padx=(10, 5), pady=(5, 5))

                value.insert(0, currency_value)
                value.configure(state='disabled')
                self.currency_widgets.append(currency)
                self.value_widgets.append(value)
                row_index += 1

        self.save_to_excel_button = ctk.CTkButton(master=self, text='Save to Excel', fg_color='#00AF22',
                                                  font=('Halvica', 14, 'bold'), hover_color='#0034B3',
                                                  command=lambda: self.open_save_details_window(
                                                      self.currency_widgets, self.value_widgets))
        self.save_to_excel_button.grid(row=16, column=1, pady=(25, 0))

        self.clear_currency_button = ctk.CTkButton(master=self, text='Clear currency', fg_color='#A21900',
                                                   font=('Halvica', 14, 'bold'), hover_color='#0034B3',
                                                   command=lambda: self.reset_currency())
        self.clear_currency_button.grid(row=16, column=3, pady=(25, 0))

        self.value_to_convert_entry.grid(row=16, column=2, pady=(25, 0))
        self.value_to_convert_entry.bind('<Return>', self.split_value_currency)

    def split_value_currency(self, placeholder) -> None:
        """
        Split the text from the currency label and extract the value and the currency.

        Parameters:
            placeholder (event): A placeholder for the 'Return' event.
        """
        input_string = self.value_to_convert_entry.get()
        currency_pattern = r'[A-Z]{3}'

        match = re.search(currency_pattern, input_string)

        if match:
            currency_code = match.group()
            value_substring = input_string[:match.start()]
            value_substring = float(value_substring)
        else:
            print("Currency code not found in the input string.")

        try:
            self.update_values(value_substring, currency_code)
        except Exception as e:
            print(e)

    def update_values(self, value: float, currency: str) -> None:
        """
        Update the displayed values for currency conversion.

        Parameters:
            value: The numerical value to convert.
            currency: The currency code for conversion.
        """
        cc = CurrencyConvertor(currency)
        cc.fetch_all_details()
        exchange_rates = cc.exchange_rates
        for index, widget in enumerate(self.value_widgets):
            user_value = round(float(exchange_rates[self.currency_widgets[index].cget('text')]), 2)
            converted_value = round((float(value) * user_value), 2)
            widget.configure(state='normal')
            widget.delete(0, 'end')
            widget.insert(0, str(converted_value))
            widget.configure(state='disabled')

    def reset_currency(self) -> None:
        """
        Reset the currency converter to its default state.
        """
        self.currency_converter = CurrencyConvertor('USD')
        self.update_values(1, 'USD')
        self.value_to_convert_entry.delete(0, 'end')

    def open_save_details_window(self, currency_widgets: list[ctk.CTkLabel], value_widgets: list[ctk.CTkEntry]) -> None:
        """
        Open a window to save currency details to an Excel file.

        Parameters:
            currency_widgets (list[ctk.CTkLabel]): List of currency label widgets.
            value_widgets (list[ctk.CTkEntry]): List of value entry widgets.
        """
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = DataValidator(currency_widgets, value_widgets)
        else:
            self.toplevel_window.focus()
