from asyncio.subprocess import PIPE
import asyncio


async def run():
    proc = await asyncio.create_subprocess_exec(
        '/bin/bash', '-i', stdin=PIPE, stdout=PIPE, stderr=PIPE
    )

    async def read(stream):
        message = 'E' if stream is proc.stderr else 'O'
        while True:
            print(message, '+')
            line = await stream.readline()
            print(message, '-')
            if line:
                print(message, line)
            else:
                break

    async def write():
        # COMMANDS = b'PS1="hello\n"', b'ls sub.py', b'ls DOESNT-EXIST'
        COMMANDS = b'PS1="hello\n"', b'ls sub.py', b'ls DOESNT-EXIST', b'exit'
        for command in COMMANDS:
            proc.stdin.write(command + b'\n')
            await proc.stdin.drain()
            await asyncio.sleep(0.2)

        print('terminate')
        # proc.kill()
        print('terminated')
        print('proc', dir(proc))
        print('proc.stdout', dir(proc.stdout))

    await asyncio.gather(
        read(proc.stderr),
        read(proc.stdout),
        write(),
    )


asyncio.run(run())
