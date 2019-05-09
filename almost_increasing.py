    def almost_increasing(*items):
        previous = None
        increasing = True

        for i in items:
            if previous is None or previous < i:
                previous = i
            elif increasing:
                increasing = False
            else:
                return False

        return True


    assert almost_increasing()
    assert almost_increasing(1)
    assert almost_increasing(1, 2)
    assert almost_increasing(2, 1)
    assert almost_increasing(1, 1)
    # Actually, any sequence of length 2 or less is almost_increasing

    assert almost_increasing(1, 2, 5)
    assert almost_increasing(2, 1, 3)
    assert almost_increasing(1, 3, 2)
    assert almost_increasing(1, 3, 2, 5)
    assert almost_increasing(1, 1, 2, 5)

    assert not almost_increasing(1, 1, 1)
    assert not almost_increasing(2, 1, 1)
    assert not almost_increasing(3, 2, 1)
    assert not almost_increasing(5, 1, 2)
    assert not almost_increasing(1, 1, 2, 5, 5)
