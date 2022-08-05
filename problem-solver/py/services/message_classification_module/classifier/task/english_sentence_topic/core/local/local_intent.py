"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""

from typing import Any, Dict

from message_classification_module.classifier.task.english_sentence_topic.core.constants.constants import (
    Intent,
    Utterance,
)
from message_classification_module.classifier.task.english_sentence_topic.core.local.local_data import LocalData
from message_classification_module.classifier.task.english_sentence_topic.core.wit_action import WitIntentAction


class LocalIntentFromIntent(LocalData):
    def set_from_intent(self, wit_intent_response: Dict[str, Any]) -> None:
        """

        :param wit_intent_response:
        :return: action dict if action, else empty dict

        Example of wit_intent_response:
        {
            "id": 777,
            "name": "intent_name",
            "entities": [],
            "traits": []
        }
        """
        intent_name = wit_intent_response[Intent.NAME.value]
        if intent_name not in self.data:
            self.data.add(intent_name)


class LocalIntentFromUtterance(LocalData):
    def __init__(self):
        """
        Set a local intent from wit.ai utterance json response
        """
        super().__init__()
        self.actions = WitIntentAction()

    def set_from_utterance(self, utterance_json: Dict[str, Any]) -> Dict[str, str]:
        """
        :param utterance_json:
        :return:

        Example of wit_utterance_response:
        {
            "intent": "intent_name"
        }
        """
        self.actions.clear()
        intent_name = utterance_json[Utterance.INTENT.value]
        if intent_name not in self.data:
            self.data.add(intent_name)
            self.actions.set_intent_action(intent_name=intent_name)
        return self.actions.get()


class LocalIntent(LocalIntentFromIntent, LocalIntentFromUtterance):
    pass
