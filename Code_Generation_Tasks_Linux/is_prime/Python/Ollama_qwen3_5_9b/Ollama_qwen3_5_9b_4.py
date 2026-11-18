def is_prime(number: int) -> bool:
    if number <= 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False
    limit = int(number ** 0.5) + 1
    for i in range(3, limit, 2):
        if number % i == 0:
            return False
    return True