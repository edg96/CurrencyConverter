import os.path

import pandas as pd
import customtkinter as ctk


class ExcelConverter:
    """
    The ExcelConverter class is responsible for extracting the data from the main window and
    providing all the methods necessary for storing the corresponding data into an Excel file.

    Attributes:
        _saving_location (str): The directory where the CSV file will be saved.
        _excel_name (str): The name of the Excel file (without the file extension).
        _currency_widgets (list[ctk.CTkLabel]): A list of currency label widgets.
        _value_widgets (list[ctk.CTkEntry]): A list of value entry widgets.

    Note:
    - The class is saving the data into a CSV file type.
    """
    def __init__(self, saving_location: str, excel_name: str, currency_widgets: list[ctk.CTkLabel],
                 value_widgets: list[ctk.CTkEntry]):
        self._saving_location = saving_location
        self._excel_name = excel_name
        self._currency_widgets = currency_widgets
        self._value_widgets = value_widgets

    @property
    def saving_location(self):
        return self._saving_location

    @property
    def excel_name(self):
        return self._excel_name

    def extract_currency_from_widgets(self) -> list[str]:
        """
        Extract currency names from the currency label widgets.

        Returns:
            list[str]: A list of currency names.
        """
        currencies = [currency_widget.cget('text') for currency_widget in self._currency_widgets]
        return currencies

    def extract_values_from_widgets(self) -> list[float]:
        """
        Extract numerical values from the value entry widgets.

        Returns:
            list[float]: A list of numerical values.
        """
        values = [float(value_widget.get()) for value_widget in self._value_widgets]
        return values

    def _construct_currency_values(self) -> dict[str, float]:
        """
        Construct a dictionary with currency-value pairs.

        Returns:
            dict[str, float]: A dictionary with currency names as keys and their respective values
            as values.
        """
        currencies, values = self.extract_currency_from_widgets(), self.extract_values_from_widgets()
        currencies_and_values = {currency: values[index] for index, currency in enumerate(currencies)}
        return currencies_and_values

    def export_to_csv(self) -> None:
        """
        Export currency and value data to a CSV file.
        """
        currencies_and_values = self._construct_currency_values()
        data = [{'Currency': currency, 'Value': value} for currency, value in currencies_and_values.items()]
        df = pd.DataFrame(data=data)
        df.to_csv(os.path.join(self.saving_location, self.excel_name + '.csv'), encoding='utf-8', index=False)
