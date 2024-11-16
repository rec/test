import dis

code = """\
def func(dtype):
    return dtype in {32, 2, 16}
"""

print(dis.dis(code))
