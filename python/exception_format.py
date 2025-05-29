class C:
    def __str__(self):
        return "string"

    def __repr__(self):
        return "REPR"


print(ValueError(C()))
