"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""


def is_built_in(value: str) -> bool:
    return value.startswith("wit$")
