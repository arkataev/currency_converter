def exchange(exchange_rate: float, amount: float) -> float:
    """Converts amount using exchange rate"""
    if exchange_rate < 0:
        raise ValueError(f'Expected exchange_rate to be > 0, given {exchange_rate}')
    elif amount < 0:
        raise ValueError(f'Expected amount to be > 0, given {amount}')
    return exchange_rate * amount
