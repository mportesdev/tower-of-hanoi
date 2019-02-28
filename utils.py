def even_steps(start, stop, n, include_stop=True, decimal_places=6):
    """Yields a sequence of 'n' evenly increasing numbers between 'start'
    and 'stop'.

    Examples:
    >>> list(even_steps(0, 100, 5))
    [0.0, 25.0, 50.0, 75.0, 100.0]

    >>> list(even_steps(0, 100, 5, include_stop=False))
    [0.0, 20.0, 40.0, 60.0, 80.0]

    >>> list(even_steps(2, 3, 4))
    [2.0, 2.333333, 2.666667, 3.0]

    >>> list(even_steps(2, 3, 4, decimal_places=2))
    [2.0, 2.33, 2.67, 3.0]
    """

    if include_stop:
        step = (stop - start) / (n - 1)
    else:
        step = (stop - start) / n

    for i in range(n):
        value = start + i * step
        yield round(value, decimal_places)
