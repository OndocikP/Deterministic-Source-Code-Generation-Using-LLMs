
def is_prime(number: int) -> bool:
    if number < 2:
        return False

    limit = int(number ** 0.5)
    for divisor in range(2, limit + 1):
        if number % divisor == 0:
            return False

    return True
