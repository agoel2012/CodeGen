#!/usr/bin/python3

from langgen import LangGen
from typing import List

class CppGen(LangGen):
    def __init__(self, author="", mock_attr=False):
        self.mock_attr = mock_attr
        super().__init__(author, "C++", ".hpp")

    def add_function_definition(self, **kwargs) -> str:
        func_str = ""
        if kwargs['doxygen_ready'] is True:
            func_str = "\n\n/**\n * @brief {}\n".format(kwargs['func_name'])
            for index, arg in enumerate(kwargs['arguments']):
                func_str += " * @param {}\n".format(arg)

            func_str += " * @return {}\n".format(kwargs['ret_val'])
            func_str += " */"

        if self.mock_attr:
            func_str += "\n virtual "
        else:
            func_str += "\n"

        func_str += "{} {}(".format(kwargs['ret_val'], kwargs['func_name'])
        for index, arg in enumerate(kwargs['arguments']):
            if index == len(kwargs['arguments']) - 1:
                func_str += ("{}".format(arg))
            else:
                func_str += ("{}, ".format(arg))

        if self.mock_attr:
            func_str += ") = 0;\n"
        else:
            func_str += ");\n"
        return func_str


    def add_class_definition_begin(self, **kwargs) -> str:
        if kwargs.get('derived_class', None) is None:
            class_str = "\nclass {0}".format(kwargs['base_class'])
        else:
            class_str = "\nclass {0} : public {1}".format(kwargs['derived_class'], kwargs['base_class'])

        class_str += " {\n public: \n"
        if self.mock_attr:
            class_str += " virtual ~{0}() ".format(kwargs['base_class'] if kwargs.get('derived_class', None) is None else kwargs['derived_class'])
            class_str += " {}\n"

        return class_str

    def add_class_definition_end(self) -> str:
       return "\n};\n"

    def add_includes(self, includes: List[str]) -> str:
        include_str = ""
        begin_encap = ""
        end_encap = ""
        if self.mock_attr:
            include_str += "\n#include <gmock/gmock.hpp>\n#include <gtest/gtest.hpp>\n"
            begin_encap = "\nextern \"C\" {\n"
            end_encap = "\n}\n"

        prefix_str = "#include <"
        suffix_str = ">"
        updated_includes = [prefix_str + header + suffix_str for header in includes]
        include_str += begin_encap
        include_str += "\n".join(updated_includes)
        include_str += end_encap
        return include_str
