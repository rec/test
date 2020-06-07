import asyncio
from subprocess import PIPE


async def run(shell, commands, callback, echo):
    proc = await asyncio.create_subprocess_shell(
        ' '.join(shell),
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE)

    async def read(stream):
        is_err = stream is proc.stderr
        while True:
            line = await stream.readline()
            if not line:
                break
            callback(is_err, line.decode('utf8').rstrip('\n'))

    async def write(stream):
        for command in commands:
            e = echo.format(command)
            stream.write((command + '\n').encode('utf8'))
            await stream.drain()
            await asyncio.sleep(0.01)
            # TODO: sleep is wrong!  I really want to wait for the prompt

        proc.terminate()

    await asyncio.gather(
        write(proc.stdin),
        read(proc.stderr),
        read(proc.stdout),
    )


def yield_inputs():
    while True:
        s = input('$ ')
        if not s:
            break
        yield s


def main():
    asyncio.run(run(('/bin/bash', '-i'), yield_inputs(), print, "echo '{}'"))


if __name__ == '__main__':
    main()
