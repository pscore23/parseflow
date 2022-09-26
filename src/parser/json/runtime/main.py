import ast
import builtins
import io
import os
import re
import sys

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


class JSONParser:
    def __init__(self):
        self._setup()

        with builtins.open(rf"{os.getcwd()}\src\parser\json\define\grammar.lark", "r", encoding="utf-8") as gf:
            self.grammar = Lark(gf, start="value", parser="lalr", lexer="standard",
                                propagate_positions=False, maybe_placeholders=False, transformer=_TreeToJSON())

    def _setup(self):
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    def parse(self, text):
        try:
            return ast.literal_eval(str(self.grammar.parse(text.translate(str.maketrans({"'": "\""})))))

        except exceptions.UnexpectedInput as e:
            hint = re.findall(r"\d+", str(e))[::-1][:2:]

            raise _exceptions.ParsingError(f"""JSON のパースを試みましたが失敗しました:
                                            理由 - JSON が破損しています
                                            破損している箇所 - {hint[1]} 行目の {hint[0]} 文字目""")
