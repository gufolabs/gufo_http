import asyncio
import sys

from gufo.http.async_client import HttpClient


async def main(url: str) -> None:
    async with HttpClient() as client:
        r = await client.get(url)
        if r.status != 200:
            print(f"Invalid response code: {r.status}")
            return
        data = await r.read()
        print(data)


asyncio.run(main(sys.argv[1]))
