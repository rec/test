import sys

USE_LINES = not True


def chunk(it):
    buffer = []
    was_indented = False

    for line in it:
        line = line.rstrip()
        is_indented = not line or line.startswith(' ')
        if was_indented != is_indented:
            was_indented = is_indented
            if buffer:
                yield buffer
            buffer = []
        buffer.append(line)

    if buffer:
        yield buffer


def count_commits():
    chunks = list(chunk(sys.stdin))
    assert len(chunks) % 2 == 0

    id_to_size = {}
    size_to_ids = {}

    for header, message in zip(*([iter(chunks)] * 2)):
        commit, commit_id, *_ = header[0].split()
        assert commit == 'commit'
        assert len(commit_id) == 40
        assert all(not line or line.startswith('    ') for line in message)
        if USE_LINES:
            size = len(message) - 1
        else:
            size = sum(len(line) - 3 if line else 1 for line in message) - 1
        commit_id = commit_id[:10]
        id_to_size[commit_id] = size
        size_to_ids.setdefault(size, []).append(commit_id)

    return id_to_size, size_to_ids


def report_commits():
    id_to_size, size_to_ids = count_commits()
    items = sorted(size_to_ids.items())
    little = items[:5]
    big = items[-20:]
    import statistics
    print({
        'little': little,
        'big': big,
        'mean': statistics.mean(size_to_ids.keys()),
        'median': statistics.median(size_to_ids.keys()),
    })

if __name__ == '__main__':
    report_commits()
