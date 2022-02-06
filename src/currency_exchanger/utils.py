def is_valid_cc(currency_code: str) -> bool:
    """Checks if currency code complies to ISO 4217"""
    if not type(currency_code) is str:
        raise TypeError(f'Expected currency code to be string, got {type(currency_code)}')
    if not len(currency_code) == 3:
        raise ValueError(f'Expected {currency_code} length is 3, got {len(currency_code)}')
    elif not currency_code.isupper():
        raise ValueError(f'Expected {currency_code} to be upper case')
    return True
