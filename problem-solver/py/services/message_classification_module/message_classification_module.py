"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Nikiforov Sergei
Author Kseniya Bantsevich
Author Anastasiya Vasilevskaya
"""

from common import ScModule, ScPythonEventType

from common.sc_log import Log
from common_module.keynode.global_sc_keynodes import GlobalScKeynodes
from common_module.constant.identifiers import CommonIdentifiers

from common_module.searcher.common_constructions_searcher import is_action_deactivated

from message_classification_module.message_topic_classification_agent import MessageTopicClassificationAgent
from message_classification_module.constants.identifiers import ClassificationIdentifiers


class MessageClassificationModule(ScModule):
    def __init__(self):
        identifiers = [id.value for id in ClassificationIdentifiers]
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
        if is_action_deactivated(self.ctx, ClassificationIdentifiers.ACTION_MESSAGE_TOPIC_CLASSIFICATION.value):
            self.log.debug('Action "action_message_topic_classification" is deactivated')
        else:
            self.log.debug('Action "action_message_topic_classification" is activated')
            classification_agent = MessageTopicClassificationAgent(self)
            classification_agent.Register(
                self.keynodes[CommonIdentifiers.QUESTION_INITIATED.value], ScPythonEventType.AddOutputEdge
            )

    def OnShutdown(self):
        self.log.info("Shutting down the message classification module")


service = MessageClassificationModule()
service.Run()
