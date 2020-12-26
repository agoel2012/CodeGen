#!/usr/bin/python3

from abc import abstractmethod
from typing import List

class LangGen:
    def __init__(self, author="",
                 language="",
                 header_ext=""):
        self.author = author
        self.language = language
        self.header_ext = header_ext

    def add_copyright(self) -> str:
        return "/** Copyright (c) 2020 {} **/\n".format(self.author)

    def add_file_doxygen_guard(self, filename: str) -> str:
        return "\n/**\n * @file {}\n * @brief Contains datatypes, definitions for {} module \n * @author {} \n */\n".format((filename + self.header_ext), filename, self.author)

    def add_headerguard_begin(self, filename: str) -> str:
        return "#ifndef {0}_{1}\n#define {0}_{1}\n".format(filename.upper(), self.header_ext.split('.')[1].upper())

    def add_headerguard_end(self, filename: str) -> str:
        return "\n#endif /*! {0}_{1} */\n".format(filename.upper(), self.header_ext.split('.')[1].upper())

    @abstractmethod
    def add_function_definition(self, **kwargs) -> str:
        raise NotImplementedError("{0} language specific feature not supported".format(self.language))

    @abstractmethod
    def add_includes(self, includes: List[str]) -> str:
        raise NotImplementedError("{0} language specific feature not supported".format(self.language))

    @abstractmethod
    def add_class_definition_begin(self, **kwargs) -> str:
        raise NotImplementedError("{0} language specific feature not supported".format(self.language))

    @abstractmethod
    def add_class_definition_end(self) -> str:
        raise NotImplementedError("{0} language specific feature not supported".format(self.language))
