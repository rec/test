def paged_queries(**kwargs):
    continuation = None

    while True:
        result = jon_query(**kwargs, continuation=continuation)

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


def all_children_simple(node):
    yield node

    for child in jon_direct_children(node):
        for descendent in all_children_simple(child):
            yield descendent


def all_children(node):
    yield node

    for child in jon_direct_children(node):
        yield from all_children(child)
