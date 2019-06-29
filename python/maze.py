def find_path(grid, x, y, path, memoize=None):
    try:
        if not grid[y][x]:
            return
    except:
        return

    if x == len(grid[y]) - 1 and y == len(grid) - 1:
    path.append((x, y))
    if xend and yend:
        return path
