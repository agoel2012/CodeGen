#!/usr/bin/python3

from langgen import LangGen
from typing import List


class CGen(LangGen):
    def __init__(self, author):
        super().__init__(author, "C", ".h")

    def add_function_definition(self, **kwargs) -> str:
        func_str = ""
        if kwargs['doxygen_ready'] is True:
            func_str = "\n\n/**\n * @brief {}\n".format(kwargs['func_name'])
            for index, arg in enumerate(kwargs['arguments']):
                func_str += " * @param {}\n".format(arg)

            func_str += " * @return {}\n".format(kwargs['ret_val'])
            func_str += " */"

        func_str += "\n{} {}(".format(kwargs['ret_val'], kwargs['func_name'])
        for index, arg in enumerate(kwargs['arguments']):
            if index == len(kwargs['arguments']) - 1:
                func_str += ("{}".format(arg))
            else:
                func_str += ("{}, ".format(arg))

        func_str += ");\n"
        return func_str

    def add_includes(self, includes: List[str]) -> str:
        prefix_str = "#include <"
        suffix_str = ">"
        updated_includes = [
            prefix_str + header + suffix_str for header in includes
        ]
        include_str = "\n".join(updated_includes)
        return include_str
