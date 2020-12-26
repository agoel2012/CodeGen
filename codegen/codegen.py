#!/usr/bin/python3

import sys
import os
import argparse
import json
from argparse import Namespace
from typing import Dict
from collections import defaultdict
import logging

log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO' : logging.INFO,
    'WARNING' : logging.WARNING,
    'ERROR' : logging.ERROR,
    'CRITICAL' : logging.CRITICAL
}

def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(description='Generate C/C++ sources from JSON schema')
    parser.add_argument('--json-file', type=str,
                        help='path to JSON schema file')
    parser.add_argument('--log-level', type=str,
                        default='INFO',
                        choices=log_levels.keys(),
                        help='Log level for the script')
    args = parser.parse_args()
    return args

def setup_logging(level_str: str):
    log_level = log_levels.get(level_str, None)
    if log_level is None:
        log_level = logging.WARNING # Force warnings only

    log_params = {
        'level' : log_level,
        'format' : '%(asctime)s__[%(levelname)s, %(module)s.%(funcName)s](%(name)s)__[L%(lineno)d] %(message)s'
    }

    logging.basicConfig(**log_params)

def parse_json_dict(js: str) -> Dict:
    logging.info("JSON Schema to process: {0}".format(js))
    with open(js) as fl:
        data = json.load(fl) # Dict[str, str]
    return (data)

def display_dict(d: Dict) -> None:
    for k, v in d.items():
        logging.debug("key: {}, value: {}".format(k, v))

def main() -> None:
    args = parse_args()
    setup_logging(args.log_level)
    if os.path.exists(args.json_file):
        json_dict = parse_json_dict(args.json_file)
        display_dict(json_dict)


if __name__ == '__main__':
    py_ver = (sys.version_info.major, sys.version_info.minor)
    assert py_ver >= (3,7)
    main()
