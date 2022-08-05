"""
    Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

import time
from datetime import datetime
from unittest import TestLoader, TestSuite, TextTestRunner

from common import ScModule
from common.sc_log import Log
from common_module.exception.custom_exception import CustomException
from common_module.keynode.global_sc_keynodes import GlobalScKeynodes
from sc import ScAddr, ScMemoryContext, ScType

COMMON_WAIT_TIME = 30


def wait_agent(ctx: ScMemoryContext, seconds: int, question_node: ScAddr, reaction_node: ScAddr):
    start = datetime.now()
    delta = 0
    while not ctx.HelperCheckEdge(reaction_node, question_node, ScType.EdgeAccessConstPosPerm) and delta < seconds:
        delta = (datetime.now() - start).seconds
        time.sleep(0.1)


def run_tests(module: ScModule, tests: tuple):
    suite = TestSuite()
    for test_item in tests:
        test_names = TestLoader().getTestCaseNames(test_item)
        for test_name in test_names:
            suite.addTest(test_item(test_name, module))
    res = TextTestRunner(verbosity=2).run(suite)
    if not res.wasSuccessful():
        raise CustomException("Unit test failed.")


class TestModule(ScModule):
    def __init__(self, test_cases: tuple, ctx, cpp_bridge):
        ScModule.__init__(self, ctx=ctx, cpp_bridge=cpp_bridge, keynodes=[])
        self.keynodes = GlobalScKeynodes(self.ctx)
        self.log = Log(self.__class__.__name__)
        self.test_cases = test_cases

    def do_tests(self):
        try:
            run_tests(self, self.test_cases)
        except CustomException as ex:
            self.log.error(str(ex))
        finally:
            self.Stop()

    def OnInitialize(self, params):  # pylint: disable=unused-argument
        self.do_tests()
