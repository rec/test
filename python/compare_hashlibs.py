import hashlib, timeit


def run_hash(hasher):
    h = hasher()
    h.update(b'https://www.grainger.com/product/WIDIA-GTD-Spiral-Flute-Tap-53MX14')
    return h.hexdigest()


def run():
    for k, v in vars(hashlib).items():
        if not k.startswith('_') and callable(v):
            try:
                t = timeit.timeit(lambda: run_hash(v))
                print(k, t)
            except Exception:
                pass

run()
