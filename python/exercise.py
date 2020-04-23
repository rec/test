def product(a, b):
    ax, ay = len(a[0]), len(a)
    bx, by = len(b[0]), len(b)

    assert all(len(row) == ax for row in a)
    assert all(len(row) == bx for row in b)
    assert ax == by

    result = []
    for i in range(ay):
        row = []
        result.append(row)
        for j in range(bx):
             row.append(sum(a[i][k] * b[k][j] for k in range(ax)))
    return result


# https://www.mathsisfun.com/algebra/matrix-multiplying.html
a = [
    [1, 2, 3],
    [4, 5, 6]
]
b = [
    [7, 8],
    [9, 10],
    [11, 12]
]
print(product(a, b))
