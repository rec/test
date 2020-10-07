import asyncio


async def main():
    async def one():
        await asyncio.sleep(1)
        return 'one'

    async def two():
        await asyncio.sleep(1.25)
        return 'two'

    return await asyncio.gather(one(), two())


print('XXX', asyncio.run(main()))
