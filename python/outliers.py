import statistics

def remove_outliers(vec: list[float]) -> list[float]:
    mu = statistics.fmean(vec)
    sigma = statistics.stdev(vec)
    normed = [(mu - i) / sigma for i in vec]
    return [v for v, n in zip(vec, normed) if -2 < n < 2]
