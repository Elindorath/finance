import time
from contextlib import contextmanager


@contextmanager
def timed_performance(prefix: str = None):
    start = time.perf_counter()

    try:
        yield
    finally:
        elapsed_time = time.perf_counter() - start

        if elapsed_time > 1:
            printable_time = f"{elapsed_time}s"
        else:
            printable_time = f"{elapsed_time * 1000}ms"

        print(f"{prefix or 'Executed'} in {printable_time}")
