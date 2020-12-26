#!/usr/bin/python3

import sys
import os
import argparse
import json
from argparse import Namespace
from typing import Dict, List
from collections import defaultdict
import logging

AUTHOR = "Arnav Goel"
GEN_DIR = str(os.getcwd()) + '/gen'

LOG_LEVELS = {
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
                        choices=LOG_LEVELS.keys(),
                        help='Log level for the script')
    args = parser.parse_args()
    return args

def setup_logging(level_str: str):
    log_level = LOG_LEVELS.get(level_str, None)
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

def _add_C_copyright() -> str:
    return "/** Copyright (c) 2020 {} **/\n".format(AUTHOR)

def _add_C_file_doxygen_guard(filename: str) -> str:
    return "\n/**\n * @file {}\n * @brief Contains datatypes, definitions for {} module \n * @author {} \n */\n".format((filename + ".h"), filename, AUTHOR)

def _add_C_headerguard_begin(filename: str) -> str:
    return "#ifndef {}_H\n#define {}_H\n".format(filename.upper(), filename.upper())

def _add_C_headerguard_end(filename: str) -> str:
    return "\n#endif /*! {}_H */\n".format(filename.upper())

def _add_C_function_definition(ret_val: str, func_name: str, arguments: List,
                               doxygen_ready: bool) -> str:
    func_str = ""
    if doxygen_ready:
        func_str = "\n\n/**\n * @brief {}\n".format(func_name)
        for index, arg in enumerate(arguments):
            func_str += " * @param {}\n".format(arg)

        func_str += " * @return {}\n".format(ret_val)
        func_str += " */"

    func_str += "\n{} {}(".format(ret_val, func_name)
    for index, arg in enumerate(arguments):
        if index == len(arguments) - 1:
            func_str += ("{}".format(arg))
        else:
            func_str += ("{}, ".format(arg))

    func_str += ");\n"
    return func_str

def _add_C_includes(includes: List[str]) -> str:
    prefix_str = "#include <"
    suffix_str = ">"
    updated_includes = [prefix_str + header + suffix_str for header in includes]
    include_str = "\n".join(updated_includes)
    return include_str

def gen_headers(js: Dict) -> None:
    """
        0. Create a file with the filename
        1. Add copyright header
        2. Add boilerplate pragma/header-guards
        3. Build a collection of api specific include files and attach them
        4. Add global defines and data-structure definition
        5. Iterate through all API and add definitions
        6. Attach end-of-file header-guards
    """
    # Make the generated header directory
    if not os.path.exists(GEN_DIR):
        os.mkdir(GEN_DIR)
    abs_file = GEN_DIR + "/" + js['file']['name']

    # Language specific logic
    if "C" in js['languages']:
        with open(abs_file, "w") as fl:
            filename = js['file']['name'].split('.')[0]
            # Add copyright
            fl.write(_add_C_copyright())
            fl.write(_add_C_file_doxygen_guard(filename))
            # Add C header-guard begin
            fl.write(_add_C_headerguard_begin(filename))
            # Collect dependent header files
            fl.write(_add_C_includes(js['file']['include']))
            for apis in js['file']['api']:
                fl.write(_add_C_function_definition(apis['return'],
                                                    apis['name'],
                                                    apis['args'],
                                                    apis['doxygen_ready']))
            # Add C header-guard tail
            fl.write(_add_C_headerguard_end(filename))

    if "C++" in js['languages']:
        raise NotImplementedError("No support for C++ class headers")

def gen_mock_headers(js: Dict) -> None:
    pass

def gen_sources(js: Dict) -> None:
    pass

def display_dict(d: Dict) -> None:
    logging.debug(json.dumps(d))

def main() -> None:
    args = parse_args()
    setup_logging(args.log_level)
    if os.path.exists(args.json_file):
        json_dict = parse_json_dict(args.json_file)
        display_dict(json_dict)
        gen_headers(json_dict)
        gen_sources(json_dict)
        gen_mock_headers(json_dict)


if __name__ == '__main__':
    py_ver = (sys.version_info.major, sys.version_info.minor)
    assert py_ver >= (3,7)
    main()
