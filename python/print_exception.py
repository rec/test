@contextmanager
def print_exception() -> Generator[None]:
    try:
        yield
    except Exception:
        traceback.print_exc()
        raise
