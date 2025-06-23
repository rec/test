T = "()(()"

def longest(string: str) -> int:
    stack = runs = []

    for i, s in enumerate(string):
        if s == "(":
            stack.push(i)



def is_valid(s: str) -> bool:
    counter = 0
    for i in s:
        if counter < 0:
            break
        elif s == "(":
            counter += 1
        else:
            counter -= 1

    return counter == 0
