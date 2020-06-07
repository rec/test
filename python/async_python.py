import asyncio



async def read_stdout(stdout):
    print('read_stdout')
    while True:
        buf = await stdout.read(10)
        if not buf:
            break

        print(f'stdout: { buf }')


async def read_stderr(stderr):
    print('read_stderr')
    while True:
        buf = await stderr.read()
        if not buf:
            break

        print(f'stderr: { buf }')


async def write_stdin(stdin):
    print('write_stdin')
    for i in range(100):
        buf = f'line: { i }\n'.encode()
        print(f'stdin: { buf }')

        stdin.write(buf)
        await stdin.drain()
        await asyncio.sleep(0.5)


async def run():
    proc = await asyncio.create_subprocess_exec(
        '/usr/bin/tee',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    await asyncio.gather(
        read_stderr(proc.stderr),
        read_stdout(proc.stdout),
        write_stdin(proc.stdin))


asyncio.run(run())


from subprocess import Popen, PIPE
from threading import Thread

SHELL = False
CMD = [b'/bin/bash', b'-i']
CMD2 = [b'/usr/local/bin/python3.7', b'-i']



async def main():
    proc = await asyncio.subprocess.create_subprocess_shell(
        b' '.join(CMD), **POPEN_ARGS
    )
    proc.stdin.write(b'echo ONE\n')
    print(await proc.stdout.read(1024))
    proc.stdin.write(b'ls\n')
    print(await proc.stdout.read(2048))
    proc.stdin.write(b'exit\n')
    await proc.wait()


async def main2():
    proc = await asyncio.subprocess.create_subprocess_shell(
        b' '.join(CMD2), **POPEN_ARGS
    )
    proc.stdin.write(b'print("test")\n')
    print(await proc.stdout.read(1024))
    proc.stdin.write(b'dir()\n')
    print(await proc.stdout.read(2048))
    proc.stdin.write(b'quit()\n')
    await proc.wait()


if __name__ == '__main__':
    asyncio.run(main2())
