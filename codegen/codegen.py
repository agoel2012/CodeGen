#!/usr/bin/python3

import sys
import os
import argparse
from argparse import Namespace
from typing import Dict
from collections import defaultdict

def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(description='Generate C/C++ sources from JSON schema')
    parser.add_argument('--json-file', type=str,
                        help='path to JSON schema file')
    args = parser.parse_args()
    return args

def parse_json(json: str) -> Dict[str, str]:
    print("JSON Schema to process: {0}".format(json))
    prop_dict = defaultdict()
    prop_dict['language'] = ['C']
    return (prop_dict)

def display_dict(d: Dict[str, str]) -> None:
    for k, v in d.items():
        print("key: {}, value: {}".format(k, v))

def main() -> None:
    args = parse_args()
    if os.path.exists(args.json_file):
        language_dict = parse_json(args.json_file)
        display_dict(language_dict)


if __name__ == '__main__':
    main()
