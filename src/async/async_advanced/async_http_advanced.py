from concurrent.futures import ProcessPoolExecutor

import aiohttp
import asyncio
import json


async def fetch_url(session, url, result_queue):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                content = await response.read()
                loop = asyncio.get_event_loop()
                content = await loop.run_in_executor(ProcessPoolExecutor, json.loads(content.decode("utf-8")), content)
                await result_queue.put((url, content))
            else:
                print(f"Error: Received status code {response.status} for URL: {url}")
    except Exception as e:
        print(f"Exception for URL {url}: {e}")


async def worker(url_queue, result_queue):
    async with aiohttp.ClientSession() as session:
        while True:
            url = await url_queue.get()
            if url is None:  # Если получен сигнал завершения
                break
            await fetch_url(session, url, result_queue)
            url_queue.task_done()


async def fetch_urls(input_file, output_file):
    url_queue = asyncio.Queue()
    result_queue = asyncio.Queue()

    # Чтение URL из файла
    with open(input_file, 'r') as f:
        urls = [line.strip() for line in f.readlines()]

    # Заполнение очереди URL
    for url in urls:
        await url_queue.put(url)

    # Создание воркеров
    workers = [asyncio.create_task(worker(url_queue, result_queue)) for _ in range(5)]

    # Ожидание завершения обработки URL
    await url_queue.join()

    # Завершение воркеров
    for _ in workers:
        await url_queue.put(None)  # Сигнал завершения для воркеров
    await asyncio.gather(*workers)

    # Сохранение результатов
    results = {}
    while not result_queue.empty():
        url, content = await result_queue.get()
        results[url] = content

    with open(output_file, 'w') as f:
        for url, content in results.items():
            json_line = json.dumps({url: content})
            f.write(json_line + '\n')

if __name__ == "__main__":
    input_file = "list_urls.txt"  # Файл с URL
    output_file = "result.json"  # Файл для сохранения результатов

    asyncio.run(fetch_urls(input_file, output_file))
