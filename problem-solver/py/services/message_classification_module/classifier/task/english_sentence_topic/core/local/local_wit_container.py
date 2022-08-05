"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""

from typing import Any, Dict

from message_classification_module.classifier.task.english_sentence_topic.core.local.local_entity import (
    LocalEntityEntityFromEntity,
)
from message_classification_module.classifier.task.english_sentence_topic.core.local.local_intent import (
    LocalIntent,
)
from message_classification_module.classifier.task.english_sentence_topic.core.local.local_trait import LocalTrait


class LocalWitContainer:
    """Process the input sentence (utterance) and save its intent, entities and traits"""

    def __init__(self):
        self.local_intent_data = LocalIntent()
        self.local_entity_data = LocalEntityEntityFromEntity()
        self.local_trait_data = LocalTrait()

    def __call__(self, utterance_json: Dict[str, Any]):
        actions = {}
        intent_actions = self.local_intent_data.set_from_utterance(utterance_json=utterance_json)
        entities_actions = self.local_entity_data.append_from_utterance(utterance_json=utterance_json)
        traits_actions = self.local_trait_data.append_from_utterance(utterance_json=utterance_json)
        actions.update(intent_actions)
        actions.update(entities_actions)
        actions.update(traits_actions)
        return actions

    def append_intent(self, json_request: Dict[str, Any]):
        return self.local_intent_data.set_from_intent(json_request)

    def append_entity(self, json_request: Dict[str, Any]):
        return self.local_entity_data.append_from_entity(json_request)

    def append_trait(self, json_request: Dict[str, Any]):
        return self.local_trait_data.append_from_trait(json_request)
