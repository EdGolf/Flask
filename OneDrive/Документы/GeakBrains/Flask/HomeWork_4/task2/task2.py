from pathlib import Path
from task2_threading import download_img_threading
from task2_multiprocessing import download_img_multiprocessing
from task2_async import download_img_async
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Программа для скачивания файлов по заданным URL')
    parser.add_argument('-f', '--file', help='имя файла, содержащего список URL')
    parser.add_argument('-u', '--url', action='append', help='URL для скачивания')
    parser.add_argument('-t', action='store_true', help='Запускать скачивание в многопоточном режиме')
    parser.add_argument('-p', action='store_true', help='Запускать скачивание в многопроцессорном режиме')
    parser.add_argument('-a', action='store_true', help='Запускать скачивание в асинхронном режиме')
    parser.add_argument('-c', type=int, default=1, help='количество параллельных задач (по умолчанию 1)')
    args = parser.parse_args()

    url_list = []
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            url_list = f.readlines()

    url_list = list(map(str.strip, url_list))

    if args.url:
        url_list.extend(args.url)

    if args.t:
        download_img_threading(url_list, Path.cwd().joinpath('task2_files', 'threading'), args.c)

    if args.p:
        download_img_multiprocessing(url_list, Path.cwd().joinpath('task2_files', 'multiprocessing'), args.c)

    if args.a:
        download_img_async(url_list, Path.cwd().joinpath('task2_files', 'async'), args.c)