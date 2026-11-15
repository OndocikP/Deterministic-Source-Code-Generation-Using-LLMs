def is_prime(number: int) -> bool:
    if number <= 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    max_divisor = int(number ** 0.5) + 1
    for divisor in range(3, max_divisor, 2):
        if number % divisor == 0:
            return False
    return True