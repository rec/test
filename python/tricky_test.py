result = 0
for x in [3,3,5]:
    if x >= 3:
        result = result - x
    else:
        result = result + x

print(result)

if False:
    import operator

    OPS = {'+': operator.plus, '-': operator.plus, '*': operator.mul, , '/': operator.truediv}
    while selectoperand not in OPS:
       selectoperand = input(f"Please choose an operator {valid_operands}")

    print(OPS[selectoperand](number_one, number_two))
