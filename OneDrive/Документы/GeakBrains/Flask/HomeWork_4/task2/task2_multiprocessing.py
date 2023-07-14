import multiprocessing.process
from pathlib import Path
import requests
import time
from multiprocessing import Process, JoinableQueue, Lock


def _download_img_worker(directory: Path, queue: JoinableQueue, log_queue: JoinableQueue, lock: Lock):
    process_name = multiprocessing.process.current_process().name

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
            log_queue.put(f'Процесс {process_name} не смог загрузить файл из url {url}')
            log_queue.put(str(e))
        else:
            img_name = url.rsplit('/', 1)[1]
            file = directory.joinpath(img_name)
            with file.open('wb') as f_writer:
                f_writer.write(response.content)
            log_queue.put(f'Процесс {process_name} загрузил файл из url {url} за {time.time() - start_time:.05} с')
        queue.task_done()


def _logger(log_queue: JoinableQueue):
    while True:
        msg = log_queue.get()
        print(msg)
        log_queue.task_done()


def download_img_multiprocessing(url_list: list[str], path: Path, process_count: int):
    q = JoinableQueue()
    q_log = JoinableQueue()
    lock = Lock()

    log_process = Process(target=_logger, args=(q_log,), daemon=True, name=f'logger')
    log_process.start()

    start_time = time.time()
    q_log.put(f"Старт загрузки в многопроцессорном режиме")
    work_processes = []
    for i in range(process_count):
        new_process = Process(target=_download_img_worker, args=(path, q, q_log, lock), daemon=True, name=f'thread{i}')
        work_processes.append(new_process)
        new_process.start()

    for url in url_list:
        q.put(url)

    q.join()
    total_time = time.time() - start_time
    q_log.put(f"Загрузка окончена за {total_time:.05} с")
    q_log.join()
    log_process.terminate()
    for process in work_processes:
        process.terminate()