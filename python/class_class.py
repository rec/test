class A:
    a = 1


class B:
    def f(self):
        return 1

    class_a = A


if __name__ == '__main__':
    print(B.class_a().a)
