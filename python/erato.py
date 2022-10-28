def eratosthenes(n):
    is_prime = [False, False] + [True] * (n-2)
    for idx in range(n):
        if is_prime[idx]:
            for i in range(2*idx, n, idx):
                is_prime[i] = False
    return [idx for idx, p in enumerate(is_prime) if p]
