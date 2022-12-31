def paged_queries(**kwargs):
    continuation = None

    while True:
        result = make_your_query(**kwargs, continuation=continuation)

        if result.empty():
            break

        for i in result.items():
            yield i

        continuation = result.continuation


def simple_iterator():
    yield 1
    yield 2


def all_nodes_simple(root):
    yield root

    for child in root.children():
        for descendent in all_nodes_simple(child):
            yield descendent


def all_nodes(root):
    yield root

    for child in root.children():
        yield from all_nodes(child)
