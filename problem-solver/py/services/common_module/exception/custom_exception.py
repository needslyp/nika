"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from enum import Enum


class CustomException(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)


class CommonExceptionMessages(Enum):
    NODE_NOT_VALID = "node isn't valid"
    CONSTRUCTION_NOT_VALID = "construction isn't valid"
    LINK_EMPTY = "link is empty"
