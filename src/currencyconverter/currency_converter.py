import os
import pathlib

import requests

from bs4 import BeautifulSoup
from src.currencyconverter.auxiliar import read_from_file_by_line


DEFAULT_URL = "https://www.cursbnr.ro/"


class CurrencyConvertor:
    """
    The CurrencyConvertor class is responsible for fetching, processing, grouping and storing the
    exchange rates from the 'default_url'.

    Attributes:
        currency_for_reference (str): The reference currency code used for exchange rate conversions.
        exchange_rates (dict[str, float]): A dictionary that stores exchange rates for various
        currencies.
        url (str): The URL used to fetch currency exchange rate data.
        currencies_resource (str): The file path to a resource file containing continent-currency data.
        continents (list[str]): A list of continent names based on the continent-currency data.
        continents_and_currencies (list[str]): A list of continent and currency data read from the
        resource file.
        currency_per_continent (dict[str, dict[str, None]]): A dictionary that groups currencies by
        continent.

    Note:
        - The collected data can be saved and stored into an Excel file for later usage and analysis.
    """
    def __init__(self, currency_for_reference):
        self.currency_for_reference = currency_for_reference
        self.exchange_rates = {}
        self.url = DEFAULT_URL
        self.currencies_resource = os.path.join(pathlib.Path(__file__).resolve().parent.parent.parent,
                                                'resources', 'files', 'currency_per_category')
        self.exchange_rates = {}
        self.continents = []
        self.continents_and_currencies = []
        self.currency_per_continent = {}

    def get_exchange_rates(self) -> dict[str, float]:
        """
        Retrieve the exchange rates for various currencies relative to the reference currency.

        Returns:
            dict[str, float]: A dictionary containing currency codes as keys and their
            respective exchange rates as values.
        """
        return self.exchange_rates

    def _fetch_exchange_rates(self) -> None:
        """
        Fetch exchange rates from the web source and populate the 'exchange_rates' dictionary.
        """
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.content, 'lxml')
            table = soup.find('table', {'id': 'table-currencies'}).tbody

            for tr in table.find_all('tr'):
                td = tr.find_all('td')
                currency, value = td[0].text, td[2].text
                if currency in ['100KRW', '100HUF', '100JPY']:
                    currency = currency[3::]
                self.exchange_rates[currency] = float(value)
            self.exchange_rates['RON'] = 1.0000
        except Exception as e:
            print(e)

    def _update_rates_to_reference(self) -> None:
        """
        Update exchange rates to be relative to the reference currency.
        """
        reference_rate = self.exchange_rates.get(self.currency_for_reference, 1.000)

        for currency, value in self.exchange_rates.items():
            self.exchange_rates[currency] = round((reference_rate / value), 2)

    def _fetch_continents_and_currencies_bulk(self) -> None:
        """
        Read continent-currency data from the resource file.
        """
        continents_and_currencies = read_from_file_by_line(self.currencies_resource)
        self.continents_and_currencies = continents_and_currencies

    def _fetch_continents(self) -> None:
        """
        Extract continent names from the continent-currency data.
        """
        continents = [element for element in self.continents_and_currencies if not element.isupper()]
        self.continents = continents

    def _group_continents_currencies(self) -> None:
        """
        Group currencies by continent based on continent-currency data.
        """
        continent_currencies = {}
        for element in self.continents_and_currencies:
            if element in self.continents:
                if continent_currencies:
                    self.currency_per_continent[continent] = continent_currencies
                continent = element
                continent_currencies = {}
            else:
                if continent:
                    continent_currencies[element] = None
        if continent_currencies:
            self.currency_per_continent[continent] = continent_currencies

    def _fetch_currencies_values(self) -> None:
        """
        Populate currency values based on exchange rates.
        """
        for continent, currencies in self.currency_per_continent.items():
            for currency, value in currencies.items():
                for key in self.exchange_rates.keys():
                    if currency == key:
                        currencies[currency] = self.exchange_rates[currency]

    def fetch_all_details(self) -> None:
        """
        Fetch and organize all necessary details for currency conversion.
        """
        self._fetch_exchange_rates()
        self._update_rates_to_reference()
        self._fetch_continents_and_currencies_bulk()
        self._fetch_continents()
        self._group_continents_currencies()
        self._fetch_currencies_values()
