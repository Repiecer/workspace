import asyncio
import time
import aiohttp

def main(number):
    start = time.time()
    async def get_html(url):
        session = aiohttp.ClientSession()
        response = await session.get(url)
        await response.text()
        await session.close()
        return response
    async def request():
        url = 'https://www.baidu.com/'
        await get_html(url)
    tasks = [asyncio.ensure_future(request()) for _ in range(number)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    end = time.time()
    print(number, end-start)
for number in [5, 10, 20, 50, 100]:
    main(number)
