import threading
from threading import Thread, Lock
from queue import Queue
from pathlib import Path
import requests
import time


def _download_img_worker(directory: Path, queue: Queue, log_queue: Queue, lock: Lock):
    thread_name = threading.current_thread().name

    lock.acquire()
    if not directory.exists():
        directory.mkdir(parents=True)
    lock.release()

    while True:
        url = queue.get()
        start_time = time.time()
        try:
            response = requests.get(url)
        except Exception as e:
            log_queue.put(f'Поток {thread_name} не смог загрузить файл из url {url}')
            log_queue.put(str(e))
        else:
            img_name = url.rsplit('/', 1)[1]
            file = directory.joinpath(img_name)
            with file.open('wb') as f_writer:
                f_writer.write(response.content)
            log_queue.put(f'Поток {thread_name} загрузил файл из url {url} за {time.time() - start_time:.05} с')
        queue.task_done()


def _logger(log_queue: Queue):
    while True:
        msg = log_queue.get()
        print(msg)
        log_queue.task_done()


def download_img_threading(url_list: list[str], path: Path, thread_count: int):
    q = Queue()
    q_log = Queue()
    lock = Lock()

    log_thread = Thread(target=_logger, args=(q_log,), daemon=True, name=f'logger')
    log_thread.start()

    start_time = time.time()
    q_log.put(f"Старт загрузки в многопоточном режиме")
    work_threads = []
    for i in range(thread_count):
        new_thread = Thread(target=_download_img_worker, args=(path, q, q_log, lock), daemon=True, name=f'thread{i}')
        work_threads.append(new_thread)
        new_thread.start()

    for url in url_list:
        q.put(url)

    q.join()
    total_time = time.time() - start_time
    q_log.put(f"Загрузка окончена за {total_time:.05} с")
    q_log.join()