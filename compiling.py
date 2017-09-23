source_code = """
import time

def main():
    return time
"""

compiled = compile(source_code, '', mode='exec')
local = {}
exec(compiled, local)

print(dir(local))

print(local['main'])

local['main']()
