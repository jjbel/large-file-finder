from pathlib import Path
from sys import argv
from os.path import isfile
import os
from subprocess import run
from sys import exit


def at(values, index, default):
    try:
        return values[index]
    except IndexError:
        return default


def parse_size(size: str) -> int:
    units = {"B": 1, "KB": 2**10, "MB": 2**20, "GB": 2**30, "TB": 2**40}
    string = size.strip()
    return int(float(string[:-2])*units[string[-2:]])


ROOT_DIR = Path(at(argv, 1, default='.'))
MAX_COUNT = int(at(argv, 2, default='20'))
THRESHOLD = parse_size(at(argv, 3, default='1MB'))


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:7.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:7.1f}Yi{suffix}"


def clear():
    if os.name == 'nt':
        run(['cls'])
    else:
        run(['clear'])


files = []

try:
    for path in ROOT_DIR.glob('**/*'):
        if isfile(path):
            pair = (path, path.stat().st_size)

            if pair[1] < THRESHOLD:
                continue

            # old_files = files
            files.insert(0, pair)
            files.sort(key=lambda x: x[1], reverse=True)

            # if old_files[:MAX_COUNT] == files[:MAX_COUNT]:
            #     continue

            del files[MAX_COUNT:]

            clear()
            for file, size in files:
                print(sizeof_fmt(size), ':', file)
except KeyboardInterrupt:
    print("Exiting...")
    exit(130)
