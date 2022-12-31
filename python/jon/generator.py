def paged_queries(**kwargs):
    continuation = None

    while True:
        result = make_your_query(**kwargs, continuation=continuation)

        if result.empty():
            break

        for i in result.items():
            yield i

        continuation = result.continuation


def simple_generator():
    print('before')
    yield 1
    print('between')
    yield 2
    print('after')


def all_children_simple(root):
    yield root

    for child in root.direct_children():
        for descendent in all_children_simple(child):
            yield descendent


def all_children(root):
    yield root

    for child in root.direct_children():
        yield from all_children(child)
