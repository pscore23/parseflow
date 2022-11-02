import io
import re
import sys
from typing import Any

from lark import Lark, Transformer, exceptions, v_args

from ._exceptions import ParsingError
from .define.grammar import _JSON_DG


class _TreeToJSON(Transformer):
    @v_args(inline=True)
    def string(self, string_):
        return string_[1:-1].replace("\\\"", "\"")

    # autopep8: off
    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda self, _: False
    # autopep8: on

    array = list
    pair = tuple
    object = dict
    number = v_args(inline=True)(float)


class JSON:
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self) -> None:
        self._setup()
        self.grammar = Lark(
            grammar=_JSON_DG,
            parser="lalr",
            lexer="standard",
            propagate_positions=False,
            maybe_placeholders=False,
            transformer=_TreeToJSON()
        )

    def _setup(self) -> None:
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    def parse(self, __text: str) -> Any:
        try:
            return self.grammar.parse(__text.translate(str.maketrans({"'": "\""})))

        except exceptions.UnexpectedInput as e:
            hint: list[Any] = re.findall(r"\d+", str(e))[::-1][:2:]

            raise ParsingError(
                f"""JSON corruption: Line {hint[1]}, character {hint[0]}.""")
