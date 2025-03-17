import asyncio
import aiohttp
import json

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]


async def fetch_urls(urls: list[str], file_path: str):
    limit_of_requests = asyncio.Semaphore(5)

    async def get_info_from_url(current_session, current_url, limited_requests):
        async with limited_requests:
            try:
                async with current_session.get(current_url, timeout=5) as response:
                    return {"url": current_url, "status_code": response.status}
            except (aiohttp.ClientError, asyncio.TimeoutError):
                return {"url": current_url, "status_code": 0}

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(get_info_from_url(session, url, limit_of_requests))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        with open(file_path, 'w') as f:
            json.dump({result["url"]: result["status_code"] for result in results}, f)


if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results_as_in_tz.json'))
