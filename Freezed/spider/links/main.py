import asyncio
import time
import aiohttp
import requests
start = time.time()
async def get_url(url):
    session = aiohttp.ClientSession()
    async with session.get(url) as response:
        await session.close()
        return await response.text()

async def main(number):
    url = 'https://www.httpbin.org/delay/2'
    response = await get_url(url)
    print(str(number), 'resCode', response)
tasks = [asyncio.ensure_future(main(_)) for _ in range(5)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
end = time.time()
print(end - start)
