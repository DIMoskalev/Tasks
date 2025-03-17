import asyncio
import aiohttp
import json


async def fetch_urls(file_path: str, result_json_file_path: str):
    limit_of_requests = asyncio.Semaphore(5)

    async def get_info_from_url(current_session, current_url, limited_requests):
        async with limited_requests:
            try:
                async with current_session.get(current_url, timeout=10) as response:
                    if response.status == 200:
                        content = await response.json()
                        return {"url": current_url, "content": content}
            except (aiohttp.ClientError, asyncio.TimeoutError):
                return {"url": current_url, "message": "Invalid response"}

    async with aiohttp.ClientSession() as session:
        with open(file_path, 'r') as f:
            urls = f.read().splitlines()
        tasks = []
        for url in urls:
            task = asyncio.create_task(get_info_from_url(session, url, limit_of_requests))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        with open(result_json_file_path, 'w') as file:
            for result in results:
                if result:
                    file.write(json.dumps(result) + '\n')


if __name__ == '__main__':
    asyncio.run(fetch_urls('./list_urls.txt', './results_as_in_example.jsonl'))
