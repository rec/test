def main():
    try:
        raise ValueError('a')
    except Exception as e:
        raise TypeError('b') from None


main()
