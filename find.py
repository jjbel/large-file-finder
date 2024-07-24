#!/usr/bin/env python3

from pathlib import Path
from sys import argv
from os import name as os_name
from subprocess import run
from sys import exit


def arg(index, default):
    try:
        return argv[index]
    except IndexError:
        return default


def parse_size(size: str) -> int:
    units = {"B": 1, "KB": 2**10, "MB": 2**20, "GB": 2**30, "TB": 2**40}
    string = size.strip()
    return int(float(string[:-2])*units[string[-2:]])


ROOT_DIR = Path(arg(1, default='.'))
MAX_COUNT = int(arg(2, default='30'))
THRESHOLD = parse_size(arg(3, default='100MB'))


def sizeof_fmt(num):
    for unit in ["", "K", "M", "G"]:
        if abs(num) < 1024.0:
            return f"{num:7.1f}{unit}B"
        num /= 1024.0
    return f"{num:7.1f}TiB"


def clear():
    if os_name == 'nt':
        run(['cls'])  # or use run?
    else:
        run(['clear'])


def main():
    files = []

    for path in ROOT_DIR.glob('**/*'):
        if not path.is_file():
            continue

        pair = (path, path.stat().st_size)

        # imp for performance, as skips sorting everytime
        if pair[1] < THRESHOLD:
            continue

        # old_files = files
        files.append(pair)
        files.sort(key=lambda x: x[1], reverse=True)

        # if old_files[:MAX_COUNT] == files[:MAX_COUNT]:
        #     continue

        del files[MAX_COUNT:]

        clear()
        for file, size in files:
            print(sizeof_fmt(size), ':', file)


try:
    main()
except KeyboardInterrupt:
    print("Exiting...")
    exit(130)
