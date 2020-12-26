#!/usr/bin/python3

import sys
import os
import argparse
import json
from argparse import Namespace
from typing import Dict, List
from collections import defaultdict
import logging
from cgen import CGen
from cppgen import CppGen

AUTHOR = "Arnav Goel"
GEN_DIR = str(os.getcwd()) + '/gen'

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser(
        description='Generate C/C++ sources from JSON schema')
    parser.add_argument('--json-file',
                        type=str,
                        help='path to JSON schema file')
    parser.add_argument('--log-level',
                        type=str,
                        default='INFO',
                        choices=LOG_LEVELS.keys(),
                        help='Log level for the script')
    args = parser.parse_args()
    return args


def setup_logging(level_str: str):
    log_level = LOG_LEVELS.get(level_str, None)
    log_params = {
        'level':
        log_level,
        'format':
        '%(asctime)s__[%(levelname)s, %(module)s.%(funcName)s](%(name)s)__[L%(lineno)d] %(message)s'
    }

    logging.basicConfig(**log_params)


def parse_json_dict(js: str) -> Dict:
    logging.info("JSON Schema to process: {0}".format(js))
    with open(js) as fl:
        data = json.load(fl)  # Dict[str, str]
    return (data)


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
    if "C" != js['file']['language']:
        raise NotImplementedError(
            "No support for {} language specific codegen".format(
                js['file']['language']))

    logging.info("Generating C header: {}".format(abs_file))
    cg = CGen(AUTHOR)
    with open(abs_file, "w") as fl:
        filename = js['file']['name'].split('.')[0]
        # Add copyright
        fl.write(cg.add_copyright())
        fl.write(cg.add_file_doxygen_guard(filename))
        # Add C header-guard begin
        fl.write(cg.add_headerguard_begin(filename))
        # Collect dependent header files
        fl.write(cg.add_includes(js['file']['include']))
        for apis in js['file']['api']:
            fl.write(
                cg.add_function_definition(
                    ret_val=apis['return'],
                    func_name=apis['name'],
                    arguments=apis['args'],
                    doxygen_ready=apis['doxygen_ready']))
        # Add C header-guard tail
        fl.write(cg.add_headerguard_end(filename))


def gen_mock_headers(js: Dict) -> None:
    """
        0. Create a file with the filename
        1. Add copyright header
        2. Add boilerplate pragma/header-guards
        3. Build a collection of api specific include files and attach them
        4. Add abstract mock class definition
            4.1. Iterate through all API and add definitions
        5. Add derived mock class definition
            5.1. Iterate through all API and add definitions
        6. Attach end-of-file header-guards
    """
    # Make the generated header directory
    if not os.path.exists(GEN_DIR):
        os.mkdir(GEN_DIR)
    if js['file']['gmock_ready'] is False:
        logging.info("Skipping mock header generator for {}".format(
            js['file']['name']))
        return

    header_filename = js['file']['name']
    module_words = (header_filename.split('.')[0]).split('_')
    module_words = [word.title() for word in module_words]
    module_name = "".join(module_words)
    mock_class = True
    mockheader_filename = "Mock" + module_name + ".hpp"
    abs_file = GEN_DIR + "/" + mockheader_filename
    logging.info("Generating gMock C++ header: {}".format(abs_file))
    cppg = CppGen(AUTHOR, mock_class)
    with open(abs_file, "w") as fl:
        filename = mockheader_filename.split('.')[0]
        # Add copyright
        fl.write(cppg.add_copyright())
        fl.write(cppg.add_file_doxygen_guard(filename))
        # Add C++ header-guard begin
        fl.write(cppg.add_headerguard_begin(filename))
        # Collect dependent header files
        fl.write(cppg.add_includes([header_filename]))
        # Add base class definition
        fl.write(
            cppg.add_class_definition_begin(base_class=module_name,
                                            derived_class=None))
        # Add base API definition
        for apis in js['file']['api']:
            fl.write(
                cppg.add_function_definition(ret_val=apis['return'],
                                             func_name=apis['name'],
                                             arguments=apis['args'],
                                             doxygen_ready=not mock_class,
                                             derived_class=False))
        fl.write(cppg.add_class_definition_end())

        # Add derived class definition
        fl.write(
            cppg.add_class_definition_begin(base_class=module_name,
                                            derived_class=filename))

        # Add derived API definition
        for apis in js['file']['api']:
            fl.write(cppg.add_function_definition(ret_val=apis['return'],
                                                  func_name=apis['name'],
                                                  arguments=apis['args'],
                                                  doxygen_ready=not mock_class,
                                                  derived_class=True))

        fl.write(cppg.add_class_definition_end())

        # Add C header-guard tail
        fl.write(cppg.add_headerguard_end(filename))


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
    assert py_ver >= (3, 7)
    main()
