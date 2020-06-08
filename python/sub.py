from asyncio.subprocess import PIPE
import asyncio


async def run():
    proc = await asyncio.create_subprocess_exec(
        '/bin/bash', '-i', stdin=PIPE, stdout=PIPE, stderr=PIPE
    )

    async def read(stream):
        message = 'E' if stream is proc.stderr else 'O'
        while True:
            line = await stream.readline()
            if line:
                print(message, line)
            else:
                break

    async def write():
        for command in (b'PS1="hello\n"', b'ls sub.py', b'ls DOESNT-EXIST'):
            proc.stdin.write(command + b'\n')
            await proc.stdin.drain()
            await asyncio.sleep(0.01)
        proc.terminate()

    await asyncio.gather(
        read(proc.stderr),
        read(proc.stdout),
        write(),
    )


asyncio.run(run())
