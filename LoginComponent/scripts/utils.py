def parse_int(x):
    """
    Converts x to an integer. Returns None if it's not convertable.
    :param x: The object that has to be converted to an integer.
    :return: None if not convertable. An integer if convertable.
    """
    try:
        return int(x)
    except ValueError:
        return None
