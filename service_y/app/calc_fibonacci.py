import logging


def fibonacci(n):
    if n <= 1:
        logging.info(f"fibonacci({n}) = {n}")
        return n
    else:
        result = fibonacci(n - 1) + fibonacci(n - 2)
        logging.info(f"fibonacci({n}) = {result}")
        print('432342')
        return result
