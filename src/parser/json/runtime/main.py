import ast
import builtins
import os

from lark import Lark, Transformer, exceptions

import _exceptions


class _TreeToJSON(Transformer):
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


class JSON:
    def __init__(self, g_path=None):
        if g_path is None:
            with builtins.open(rf"{os.getcwd()}\src\parser\json\define\grammar.lark", "r", encoding="utf-8") as gf:
                self.grammar = Lark(gf, start="value", parser="lalr", transformer=_TreeToJSON())

        else:
            with builtins.open(g_path, "r", encoding="utf-8") as gf:
                self.grammar = Lark(gf, start="value", parser="lalr", transformer=_TreeToJSON())

    def parse(self, text):
        try:
            return ast.literal_eval(str(self.grammar.parse(text.translate(str.maketrans({"'": "\""})))).translate(str.maketrans({"'": "\""})))

        except exceptions.UnexpectedInput as e:
            raise _exceptions.InputError(e, "入力された JSON のパースに失敗しました - JSON が破損している可能性があります")


with open("src/parser/json/runtime/test.json", "r") as f:
    print(JSON().parse(f.read())[0])
