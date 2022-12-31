def lower_all(it):
    for i in it:
        yield i.lower()


# Or just (i.lower() for i in it)



def paged_queries(query):
    continuation = None

    while True:
        result = API_query(query, continuation=continuation)

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

    for child in API_direct_children(node):
        for descendent in all_children_simple(child):
            yield descendent


def all_children(node):
    yield node

    for child in API_direct_children(node):
        yield from all_children(child)
