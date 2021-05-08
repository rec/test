# These actually do something important...


def do_this():
    print('do_this')


def do_that():
    print('do_that')


def do_three():
    print('do_three')


# These next four functions do the same thing


def first(x):
    if x == 'one':
        do_this()
    else:
        if x == 'two':
            do_that()
        else:
            if x == 'three':
                do_thee()
            else:
                raise KeyError(x)


def second(x):
    if x == 'one':
        do_this()
    elif x == 'two':
        do_that()
    elif x == 'three':
        do_three()
    else:
        raise KeyError(x)


def third(x):
    function = FUNCTIONS[x]
    function(x)


FUNCTIONS = {'one': do_this, 'two': do_that, 'three': do_three}


def fourth(x):
    method = getattr(FOURTH, x)
    method()


class Fourth:
    def one(self):
        do_this()

    def two(self):
        do_that()

    def three(self):
        do_three()


FOURTH = Fourth()
