import builtins
import os

from lark import Lark, Transformer, exceptions

import _exceptions


class TreeToJSON(Transformer):
    def string(self, string_):
        (string_,) = string_

        return string_[1:-1]

    def number(self, number_):
        (number_,) = number_

        return float(number_)

    def null(self, _):
        return None

    def true(self, _):
        return True

    def false(self, _):
        return False

    list = list
    pair = tuple
    dict = dict


class JSONParser:
    def __init__(self, g_path=None):
        if g_path is None:
            with builtins.open(rf"{os.getcwd()}\src\parser\json\define\grammar.lark", "r", encoding="utf-8") as gf:
                self.grammar = Lark(gf, start="value", parser="lalr", transformer=TreeToJSON())

        else:
            with builtins.open(g_path, "r", encoding="utf-8") as gf:
                self.grammar = Lark(gf, start="value", parser="lalr", transformer=TreeToJSON())

    def parse(self, text):
        try:
            return str(self.grammar.parse(text.translate(str.maketrans({"'": "\""})))).translate(str.maketrans({"'": "\""}))

        except exceptions.UnexpectedInput as e:
            raise _exceptions.InputError(e, "入力された JSON のパースに失敗しました - JSON が破損している可能性があります")
