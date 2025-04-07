def split_patches(lines):
    def split(it, prefix):
        result = []
        for line in it:
            if line.startswith(prefix):
                if not result or result[-1]:
                    result.append([])
                result[-1].append(line)
        return result

    return [[split(j, "@@") for j in split(line, "diff")] for line in lines]


def _join(patches, count, by_chunk: bool = True):
    # by count, or in pieces
    def join(one_file):
        head, *patches = one_file
        lp = len(patches)
        d, m = divmod(lp, count)
        d += bool(m)
        a, b = (d, count) if by_chunk else (count, d)
        return [[head] + patches[b * i: b * (i + 1)] for i in range(a)]2

    return [join(p) for p in patches]


def _check_patches(all_patches):
    for file_patches in all_patches:
        for i, (head, *patch) in enumerate(file_patches):
            assert 3 <= len(head) <= 4  # Not sure 3 is possible, but...
            assert all(i[0].startswith("@@") for i in patch)
