from multiprocessing import Process, JoinableQueue
from pathlib import Path
import requests


def _get_url_text_worker(directory: Path, queue: JoinableQueue):
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


def get_url_text_multiprocessing(url_list: list[str], path: Path, process_count: int):
    q = JoinableQueue()
    processes = []
    for i in range(process_count):
        new_process = Process(target=_get_url_text_worker, args=(path.joinpath(f'process{i}'), q), daemon=True)
        processes.append(new_process)
        new_process.start()

    for url in url_list:
        q.put(url)

    q.join()

    for process in processes:
        process.terminate()