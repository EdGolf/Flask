from threading import Thread
from queue import Queue
from pathlib import Path
import requests


def _get_url_text_worker(directory: Path, queue: Queue):
    if not directory.exists():
        directory.mkdir(parents=True)

    while True:
        url = queue.get()
        try:
            response = requests.get(url)
        except Exception as e:
            print(f"Не удалось загрузить данные {url=}")
        else:
            file = directory.joinpath(url.replace('https://', '').replace('.', '_').replace('/', '') + '.html')
            with file.open('w', encoding='utf-8') as f_writer:
                f_writer.write(response.text)
        queue.task_done()


def get_url_text_threading(url_list: list[str], path: Path, thread_count: int):
    q = Queue()
    threads = []
    for i in range(thread_count):
        new_thread = Thread(target=_get_url_text_worker, args=(path.joinpath(f'thread{i}'), q), daemon=True)
        threads.append(new_thread)
        new_thread.start()

    for url in url_list:
        q.put(url)

    q.join()