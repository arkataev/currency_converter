def str_to_float(number: str) -> float:
    """Checks if amount is a valid number and converts to float

    :raise ValueError: if amount can't be converted to float
    """

def is_valid_cc(currency_code: str) -> bool:
    """Checks if currency code complies to ISO 4217"""
    if not len(currency_code) == 3:
        raise ValueError(f'Expected currency code length is 3, got {len(currency_code)}')
    elif not type(currency_code) == str:
        raise TypeError(f'Expected currency code to be of type string, got {type(currency_code)}')
    elif not currency_code.isupper():
        raise ValueError(f'Expected currency code to be upper case')
    return True