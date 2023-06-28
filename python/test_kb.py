from kb import replacer as sub

DATA = {
    'a': 1,
    'b': [1, 2],
    'c': {
        'd': {
            'e': True
        },
        'f': None
    }
}


def test_empty():
    assert sub({}) == {}


def test_simple():
    actual = sub({'a': 1})
    expected = {'a':  {"_content": 1, "_type": "<class 'int'>"}}
    assert actual == expected

    for depth in range(1, 5):
        actual = sub({'a': 1}, depth=depth)
        assert actual == expected


def test_simple_zero():
    source = {'a': 1}
    assert sub(source, depth=0) == source
    assert sub(source, depth=0) is not source


def test_full():
    actual = sub(DATA)

    expected = {
        "a": {
            "_content": 1,
            "_type": "<class 'int'>"
        },
        "b": {
            "_content": [
                1,
                2
            ],
            "_type": "<class 'list'>"
        },
        "c": {
            "d": {
                "e": {
                    "_content": True,
                    "_type": "<class 'bool'>"
                }
            },
            "f": {
                "_content": None,
                "_type": "<class 'NoneType'>"
            }
        }
    }
    assert actual == expected


def test_partial():
    actual = sub(DATA, depth=1)

    import json
    print(json.dumps(actual, indent=4))
    expected = {
        "a": {
            "_content": 1,
            "_type": "<class 'int'>"
        },
        "b": {
            "_content": [
                1,
                2
            ],
            "_type": "<class 'list'>"
        },
        "c": {
            "d": {
                "e": True
            },
            "f": None
        }
    }
    assert actual == expected
