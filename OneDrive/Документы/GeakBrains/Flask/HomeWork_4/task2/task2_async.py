import asyncio
import aiohttp
from pathlib import Path
import aiofiles
import aiofiles.os
import time


async def _download_img_worker(directory: Path, queue: asyncio.Queue, log_queue: asyncio.Queue):
    task_name = asyncio.current_task().get_name()

    if not directory.exists():
        await aiofiles.os.makedirs(directory, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        while True:
            url = await queue.get()
            start_time = time.time()
            try:
                async with session.get(url) as response:
                    content = await response.read()
                    img_name = url.rsplit('/', 1)[1]
                    file = directory.joinpath(img_name)
                    async with aiofiles.open(file, 'wb') as f_writer:
                        await f_writer.write(content)
                    await log_queue.put(
                        f'Задача {task_name} загрузила файл из url {url} за {time.time() - start_time:.05} с')
            except Exception as e:
                await log_queue.put(f'Задача {task_name} не смогла загрузить файл из url {url}')
                await log_queue.put(str(e))
            queue.task_done()


async def _logger(log_queue: asyncio.Queue):
    while True:
        msg = await log_queue.get()
        print(msg)
        log_queue.task_done()


async def _download_img_async(url_list: list[str], path: Path, task_count: int):
    q = asyncio.Queue()
    q_log = asyncio.Queue()

    log_task = asyncio.create_task(_logger(q_log))

    for url in url_list:
        q.put_nowait(url)

    start_time = time.time()
    q_log.put_nowait(f"Старт загрузки в асинхронном режиме")
    tasks = []
    for i in range(task_count):
        new_task = asyncio.create_task(_download_img_worker(path, q, q_log), name=f'task{i}')
        tasks.append(new_task)

    await q.join()

    total_time = time.time() - start_time
    q_log.put_nowait(f"Загрузка окончена за {total_time:.05} с")

    await q_log.join()

    for task in tasks:
        task.cancel()
    log_task.cancel()
    await asyncio.gather(*tasks, log_task, return_exceptions=True)


def download_img_async(url_list: list[str], path: Path, task_count: int):
    asyncio.run(_download_img_async(url_list, path, task_count))