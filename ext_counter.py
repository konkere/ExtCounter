#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse
from datetime import datetime


def args_parser():
    parser = argparse.ArgumentParser(description='Extensions calculation in dir (recursive).')
    parser.add_argument('-d', '--dir', type=str, help='Dir to scan.', required=False)
    parser.add_argument('-o', '--output', type=str, help='TXT file with results.', required=False)
    parser.add_argument('-s', '--sort', type=str, help='Sort by count/size.', required=False)
    arguments = parser.parse_args().__dict__
    return arguments


def size_converter(size_bytes):
    x_bytes = {
        'Gb': 1073741824,
        'Mb': 1048576,
        'Kb': 1024,
        'b': 0,
    }
    x_bytes_sorted = sorted(x_bytes.items(), key=lambda x: x[1], reverse=True)
    for (name, size_1) in x_bytes_sorted:
        if size_bytes >= size_1:
            size_round = int(round(size_bytes/size_1 if size_1 > 0 else size_bytes, 0))
            size_converted = f'{size_round} {name}'
            return size_converted


def scanner(path_for_scan, filename, sort_by):
    extensions = {}
    pattern_ext = r'.+\.([^\.]+)$'

    if not path_for_scan:
        path_for_scan = os.getenv('HOME')

    if not filename:
        filename = f'extensions_{datetime.now():%Y%m%d%H%M}.txt'

    if not sort_by and sort_by != 'size':
        sort_by = 'count'

    total_size = 0
    total_count = 0

    for root, dirs, files in os.walk(path_for_scan):
        for file in files:
            re_extension = re.match(pattern_ext, file)
            file_path = os.path.join(root, file)
            try:
                file_size = os.stat(file_path).st_size
            except FileNotFoundError:
                file_size = 0
            try:
                ext = re_extension.group(1)
            except AttributeError:
                ext = 'WITHOUT EXTENSION'
            else:
                ext = ext.lower()
            try:
                extensions[ext]
            except KeyError:
                extensions[ext] = {
                    'count': 1,
                    'size': file_size
                }
            else:
                extensions[ext]['count'] += 1
                extensions[ext]['size'] += file_size
            total_size += file_size
            total_count += 1

    sorted_extensions = sorted(extensions.items(), key=lambda x: x[1][sort_by], reverse=True)

    with open(filename, "w") as result:
        total_size = size_converter(total_size)
        result.write(f'Total files: {total_count}\nTotal size: {total_size}\n\n')
        for extension, nums in sorted_extensions:
            size = size_converter(nums["size"])
            result.write(f'{extension:<16}\t{nums["count"]:<10}\t{size:<10}\n')


if __name__ == '__main__':
    args = args_parser()
    scanner(path_for_scan=args['dir'], filename=args['output'], sort_by=args['sort'])
