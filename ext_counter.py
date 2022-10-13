#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse
from datetime import datetime


def args_parser():
    parser = argparse.ArgumentParser(description='Extensions calculation in dir (recursive).')
    parser.add_argument('-s', '--scan', type=str, help='Dir to scan.', required=False)
    parser.add_argument('-o', '--output', type=str, help='TXT file with results.', required=False)
    arguments = parser.parse_args().__dict__
    return arguments


def scanner(path_for_scan, filename):
    extensions = {}
    pattern_ext = r'.+\.([^\.]+)$'

    if not path_for_scan:
        path_for_scan = os.getenv('HOME')

    if not filename:
        filename = f'extensions_{datetime.now():%Y%m%d%H%M}.txt'

    for root, dirs, files in os.walk(path_for_scan):
        for file in files:
            re_extension = re.match(pattern_ext, file)
            try:
                ext = re_extension.group(1)
            except AttributeError:
                ext = 'WITHOUT EXTENSION'
            else:
                ext = ext.lower()
            try:
                extensions[ext]
            except KeyError:
                extensions[ext] = 1
            else:
                extensions[ext] += 1

    sorted_extensions = sorted(extensions.items(), key=lambda x: x[1], reverse=True)

    with open(filename, "w") as result:
        for extension, num in sorted_extensions:
            result.write(f'{num} - {extension}\n')


if __name__ == '__main__':
    args = args_parser()
    scanner(path_for_scan=args['scan'], filename=args['output'])
