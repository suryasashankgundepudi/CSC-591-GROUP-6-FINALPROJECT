Seed = 937162211


def rand(lo=0, hi=1):
    """
    Retruns the float value x between lo and hi
    """
    global Seed
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi - lo) * Seed / 2147483647


def rint(lo, hi):
    """
    Returns the rounded off digit of a random float value between lo and hi
    """
    return round(0.5 + rand(lo, hi))


def rnd(n, nPlaces=3):
    """
    Rounds off the digit to n number of places
    """
    return round(n * (10 ** nPlaces) + 0.5) / (10 ** nPlaces)


def cosine(a, b, c):
    """
    Get x, y from a line connecting `a` to `b`
    """
    x1 = (a ** 2 + c ** 2 - b ** 2) / ((2 * c) or 1)  # might be an issue if c is 0
    x2 = max(0.0, min(1.0, x1))  # in the incremental case, x1 might be outside 0,1
    y = abs((a ** 2 - x2 ** 2)) ** .5
    return x2, y