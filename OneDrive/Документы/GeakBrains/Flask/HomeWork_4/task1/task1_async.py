import asyncio
import aiohttp
from pathlib import Path
import aiofiles
import aiofiles.os


async def _get_url_text_worker(directory: Path, queue: asyncio.Queue):
    if not directory.exists():
        await aiofiles.os.makedirs(directory, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        while True:
            url = await queue.get()
            try:
                async with session.get(url) as response:
                    text = await response.text()
                    file = directory.joinpath(url.replace('https://', '').replace('.', '_').replace('/', '') + '.html')
                    async with aiofiles.open(file, 'w', encoding='utf-8') as f_writer:
                        await f_writer.write(text)
            except Exception as e:
                print(f"Не удалось загрузить данные {url=}")
            queue.task_done()


async def _get_url_text_async(url_list: list[str], path: Path, task_count: int):
    q = asyncio.Queue()

    for url in url_list:
        q.put_nowait(url)

    tasks = []
    for i in range(task_count):
        new_task = asyncio.create_task(_get_url_text_worker(path.joinpath(f'task{i}'), q))
        tasks.append(new_task)

    await q.join()

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)


def get_url_text_async(url_list: list[str], path: Path, task_count: int):
    asyncio.run(_get_url_text_async(url_list, path, task_count))