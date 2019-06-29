import dis
exec("""
def f():
    """ + """
    """.join(["X"+str(x)+"=" + str(x) for x in range(65539)]))

f()

print(dis.dis(f))
