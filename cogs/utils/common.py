from typing import Any


def str_period_insert(string: str, char: str, period: int):
    string_list = list(reversed(string))
    for i, _ in enumerate(string_list):
        if (i % (period + 1)) == 0:
            string_list.insert(i, char)

    return "".join(reversed(string_list)).strip()


class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self):
        return '...'


MISSING: Any = _MissingSentinel()
