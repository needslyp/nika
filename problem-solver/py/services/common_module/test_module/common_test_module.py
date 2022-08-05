"""
    Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
    Author Alexandr Zagorskiy
"""

from common_module.searcher.common_constructions_searcher import is_action_deactivated
from common_module.test_module.constant.test_constants import TestConstants
from common_module.test_module.entity.agent_test import COMMON_WAIT_TIME, TestModule
from sc import ScMemoryContext

from message_classification_module.test.message_classification_test import MessageTopicClassificationAgentTestCase
from speech_to_text_module.test.speech_to_text_test import SpeechToTextAgentTestCase
from text_to_speech_module.test.text_to_speech_test import TextToSpeechAgentTestCase


AGENT_TEST_CASES = [
    SpeechToTextAgentTestCase,
    TextToSpeechAgentTestCase,
    MessageTopicClassificationAgentTestCase,
]


def create_test_cases_tuple(ctx: ScMemoryContext) -> tuple:
    test_cases = []
    for test_case in AGENT_TEST_CASES:
        action_node = test_case.get_action_node()
        if action_node == TestConstants.NOT_ACTION.value or not is_action_deactivated(ctx, action_node):
            test_cases.append(test_case)
    return tuple(test_cases)


class CommonTestModule(TestModule):
    wait_time = COMMON_WAIT_TIME

    def __init__(self):
        TestModule.__init__(
            self,
            test_cases=create_test_cases_tuple(__ctx__),  # noqa pylint: disable=undefined-variable
            ctx=__ctx__,  # noqa pylint: disable=undefined-variable
            cpp_bridge=__cpp_bridge__,  # noqa pylint: disable=undefined-variable
        )


common_test_module = CommonTestModule()
common_test_module.Run()
