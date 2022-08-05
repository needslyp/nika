"""
    Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from abc import abstractmethod, ABC
from unittest import TestCase


class AgentTestCase(TestCase, ABC):
    def __init__(self, testname: str, module):
        super().__init__(testname)
        self.ctx = module.ctx

    @classmethod
    @abstractmethod
    def get_action_node(cls):
        raise NotImplementedError('Method "get_action_node" isn\'t implemented.')
