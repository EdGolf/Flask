import csv
from pathlib import Path
from task1_threading import get_url_text_threading
from task1_multiprocessing import get_url_text_multiprocessing
from task1_async import get_url_text_async
import time

if __name__ == '__main__':
    with open('task1_urls.csv', 'r', newline='', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, dialect='excel-tab', delimiter=';')
        url_list = [line['URL'] for line in csv_reader]

    start = time.time()
    get_url_text_threading(url_list, Path.cwd().joinpath('task1_files', 'threading'), 10)
    time_threading = time.time() - start

    start = time.time()
    get_url_text_multiprocessing(url_list, Path.cwd().joinpath('task1_files', 'multiprocessing'), 10)
    time_multiprocessing = time.time() - start

    start = time.time()
    get_url_text_async(url_list, Path.cwd().joinpath('task1_files', 'async'), 10)
    time_async = time.time() - start

    print(f'{time_threading=} {time_multiprocessing=} {time_async=}')