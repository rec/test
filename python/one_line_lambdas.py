def f() -> None:
    print(lambda::(a: int = 1, /, b: str = "", *, c: bool = False, **kwargs: Any) -> str:
        return f"{a}/{b}/{c} {kwargs=}"
    ::())


def f() -> None:
    def __lambda_34234(a: int = 1, /, b: str = "", *, c: bool = False, **kwargs: Any) -> str:
        print('multiline lambda')
        return f"{a}/{b}/{c} {kwargs=}"

    print(__lambda_34234())
