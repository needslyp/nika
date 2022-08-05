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
from sc import ScType
from text_to_speech_module.constant.synthesizer_identifiers import SynthesizerIdentifiers
from text_to_speech_module.creator.synthesizer_creator import create_synthesizer
from text_to_speech_module.text_to_speech_agent import TextToSpeechAgent


class TextToSpeechModule(ScModule):
    CREDENTIALS_PATH = "../resources/.env"

    def __init__(self):
        identifiers = [id.value for id in SynthesizerIdentifiers]
        ScModule.__init__(
            self,
            ctx=__ctx__,  # noqa pylint: disable=undefined-variable
            cpp_bridge=__cpp_bridge__,  # noqa pylint: disable=undefined-variable
            keynodes=[],
        )
        self.keynodes = GlobalScKeynodes(self.ctx)
        self.keynodes.add_keynodes(identifiers)
        self.log = Log(self.__class__.__name__)

    def OnInitialize(self, params):  # pylint: disable=unused-argument
        if is_action_deactivated(self.ctx, SynthesizerIdentifiers.ACTION_SYNTHESIZE_SPEECH.value):
            self.log.error("action_synthesize_speech is deactivated")
        else:
            self.log.info("Initialize the TextToSpeechModule")

            self.ctx.HelperResolveSystemIdtf(
                SynthesizerIdentifiers.ACTION_SYNTHESIZE_SPEECH.value, ScType.NodeConstClass
            )
            question_initiated = self.ctx.HelperResolveSystemIdtf(
                CommonIdentifiers.QUESTION_INITIATED.value, ScType.NodeConstClass
            )

            credentials_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.CREDENTIALS_PATH)
            try:
                if os.path.isfile(credentials_path):
                    load_dotenv(credentials_path)
                    synthesizer = create_synthesizer(self.ctx)
                    agent = TextToSpeechAgent(self, synthesizer=synthesizer)
                    agent.Register(question_initiated, ScPythonEventType.AddOutputEdge)
                else:
                    raise FileNotFoundError
            except FileNotFoundError:
                self.log.error('File with the name "{}" isn\'t found.'.format(credentials_path))
            except CustomException as ex:
                self.log.error(str(ex))

    def OnShutdown(self):
        self.log.info("Shutting down the TextToSpeechModule")


service = TextToSpeechModule()
service.Run()
