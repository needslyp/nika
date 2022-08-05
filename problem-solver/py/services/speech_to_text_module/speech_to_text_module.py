"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

import os

from dotenv import load_dotenv

from common import ScModule, ScPythonEventType
from common.sc_log import Log
from common_module.constant.identifiers import CommonIdentifiers
from common_module.exception.custom_exception import CustomException
from common_module.keynode.global_sc_keynodes import GlobalScKeynodes
from common_module.searcher.common_constructions_searcher import is_action_deactivated
from speech_to_text_module.constant.recognizer_constants import RecognizerIdentifiers
from speech_to_text_module.creator.recognizer_creator import create_recognizer
from speech_to_text_module.speech_to_text_agent import SpeechToTextAgent


class SpeechToTextModule(ScModule):
    CREDENTIALS_PATH = "../resources/.env"

    def __init__(self):
        identifiers = [id.value for id in RecognizerIdentifiers]
        ScModule.__init__(
            self,
            ctx=__ctx__,  # noqa #pylint: disable=undefined-variable
            cpp_bridge=__cpp_bridge__,  # noqa #pylint: disable=undefined-variable
            keynodes=[],
        )
        self.keynodes = GlobalScKeynodes(self.ctx)
        self.keynodes.add_keynodes(identifiers)
        self.log = Log(self.__class__.__name__)

    def OnInitialize(self, params):  # pylint: disable=unused-argument
        if is_action_deactivated(self.ctx, RecognizerIdentifiers.ACTION_RECOGNIZE_TEXT.value):
            self.log.error("action_recognize_text is deactivated")
        else:
            self.log.info("Initialize the SpeechToTextModule")

            question_initiated = self.keynodes[CommonIdentifiers.QUESTION_INITIATED.value]

            credentials_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.CREDENTIALS_PATH)
            try:
                if os.path.isfile(credentials_path):
                    load_dotenv(credentials_path)
                    recognizer = create_recognizer(self.ctx)
                    agent = SpeechToTextAgent(self, recognizer)
                    agent.Register(question_initiated, ScPythonEventType.AddOutputEdge)
                else:
                    self.log.error('File with the name "{}" isn\'t found.'.format(credentials_path))
            except CustomException as ex:
                self.log.error(str(ex))

    def OnShutdown(self):
        self.log.info("Shutting down the SpeechToTextModule")


service = SpeechToTextModule()
service.Run()
