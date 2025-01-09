import logging
def fibonacci(n):
    try:
        if n <= 1:
            logging.info(f"fibonacci({n}) = {n}")
            return n
        else:
            result = fibonacci(n-1) + fibonacci(n-2)
            logging.info(f"fibonacci({n}) = {result}")
            return result
    except Exception as e:
        logging.error(f"Ошибка при вычислении fibonacci({n}): {e}")


