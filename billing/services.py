from decimal import Decimal

DENOMINATIONS = [500, 100, 50, 20, 10, 5, 2, 1]

def calculate_denominations(amount):
    amount = int(amount)
    result = {}
    for denom in DENOMINATIONS:
        count = amount // denom
        result[denom] = count
        amount -= count * denom
    return result
