

def clamp(minimum, value, maximum):
    """
    Clamp the passed `value` to be between `minimum` and `maximum`, including.
    """
    return max(minimum, min(maximum, value))
