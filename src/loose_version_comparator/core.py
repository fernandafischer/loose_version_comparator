from __future__ import annotations

import re
from functools import total_ordering
from typing import List, Union

_Token = Union[int, str]

_BOUNDARY = re.compile(r"(?<=[A-Za-z0-9])(?=[^A-Za-z0-9])|(?<=[^A-Za-z0-9])(?=[A-Za-z0-9])")


def _tokenize(raw: str) -> List[_Token]:
    if not raw:
        return []
    tokens: List[_Token] = []
    for chunk in _BOUNDARY.split(raw):
        if chunk is None:
            continue
        stripped = chunk.strip()
        if not stripped:
            continue
        if not any(c.isalnum() for c in stripped):
            continue
        if stripped.isdigit():
            tokens.append(int(stripped))
        else:
            tokens.append(stripped)
    while tokens and type(tokens[-1]) is int and tokens[-1] == 0:
        tokens.pop()
    return tokens


@total_ordering
class Version:
    __slots__ = ("_raw", "_tokens")

    def __init__(self, raw: str) -> None:
        if not isinstance(raw, str):
            raise TypeError(f"Version expects a str, got {type(raw).__name__}")
        self._raw = raw
        self._tokens = _tokenize(raw)

    @property
    def raw(self) -> str:
        return self._raw

    @property
    def tokens(self) -> List[_Token]:
        return list(self._tokens)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return self._tokens == other._tokens

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return _tokens_lt(self._tokens, other._tokens)

    def __hash__(self) -> int:
        return hash(tuple(self._tokens))

    def __repr__(self) -> str:
        return f"Version({self._raw!r})"


def _tokens_lt(a: List[_Token], b: List[_Token]) -> bool:
    for left, right in zip(a, b):
        if type(left) is int and type(right) is int:
            if left != right:
                return left < right
            continue
        if type(left) is int and isinstance(right, str):
            return False
        if isinstance(left, str) and type(right) is int:
            return True
        assert isinstance(left, str) and isinstance(right, str)
        if left != right:
            return left < right
        continue

    if len(a) == len(b):
        return False
    if len(a) < len(b):
        return _extra_makes_greater(b[len(a):])
    return not _extra_makes_greater(a[len(b):])


def _extra_makes_greater(extras: List[_Token]) -> bool:
    for tok in extras:
        if type(tok) is int:
            if tok > 0:
                return True
            continue
        return False
    return False


def compare(a: str, b: str) -> int:
    va, vb = Version(a), Version(b)
    if va < vb:
        return -1
    if va > vb:
        return 1
    return 0
