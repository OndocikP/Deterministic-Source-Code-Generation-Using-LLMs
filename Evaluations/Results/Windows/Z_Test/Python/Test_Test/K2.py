
def is_prime(number: int) -> bool:
    if number <= 1:
        return False
    if number == 2:
        return True
    if number % 2 == 0:
        return False

    candidate = 3
    while candidate * candidate <= number:
        if number % candidate == 0:
            return False
        candidate += 2

    return True
