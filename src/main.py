from src.currencyconverter.currency_converter_window import CurrencyConverterWindow


__author__ = 'Dragos-Gabriel Enache'
__copyright__ = 'N/A'
__credits__ = ['N/A']

__license__ = 'N/A'
__version__ = "1.0.1"
__maintainer__ = 'Dragos-Gabriel Enache'
__email__ = 'edragosgabriel@gmail.com'
__status__ = 'Development'

__all__ = []


if __name__ == '__main__':
    currencyconverter = CurrencyConverterWindow()
    print(f'Author: {__author__}')
    print(f'Copyright: {__copyright__}')
    print(f'Credits: {__credits__}')

    print(f'License: {__license__}')
    print(f'Version: {__version__}')
    print(f'Maintainer: {__maintainer__}')
    print(f'Email: {__email__}')
    print(f'Status: {__status__}')

    currencyconverter.mainloop()
