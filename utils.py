def add(a: float, b: float) -> float:
    """
    Returns the sum of two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Raises:
        TypeError: If either a or b is not a number.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be numbers")
    return a + b

def subtract(a: float, b: float) -> float:
    """
    Returns the difference of two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Raises:
        TypeError: If either a or b is not a number.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be numbers")
    return a - b