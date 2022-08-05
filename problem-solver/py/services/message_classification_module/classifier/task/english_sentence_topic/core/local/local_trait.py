"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""

from typing import Any, Dict, List

from message_classification_module.classifier.task.english_sentence_topic.core.constants.constants import (
    Trait,
    TraitValue,
    Utterance,
    UtteranceTrait,
)
from message_classification_module.classifier.task.english_sentence_topic.core.local.local_data import LocalData
from message_classification_module.classifier.task.english_sentence_topic.core.wit_action import WitTraitAction


class LocalTraitFromTrait(LocalData):
    def append_from_trait(self, trait: Dict[str, Any]):
        trait_name = trait[Trait.NAME.value]
        if not self.data.get(trait_name, False):
            self._append_trait_from_trait(trait_name=trait_name, values=trait[Trait.VALUES.value])
        else:
            self._append_value_from_trait(trait_name=trait_name, values=trait[Trait.VALUES.value])

    def _append_trait_from_trait(self, trait_name: str, values: List[Dict[str, str]]):
        local_values = set()
        for value in values:
            local_values.add(value[TraitValue.VALUE.value])
        self.data[trait_name] = local_values

    def _append_value_from_trait(self, trait_name: str, values: List[Dict[str, str]]):
        local_values = self.data[trait_name]
        for value in values:
            value_name = value[TraitValue.VALUE.value]
            if value_name not in local_values:
                local_values.add(value_name)


class LocalLocalFromUtterance(LocalData):
    def __init__(self):
        """
        Set a local trait from wit.ai trait json response
        """
        super().__init__()
        self.actions = WitTraitAction()

    def append_from_utterance(self, utterance_json: Dict[str, Any]):
        self.actions.clear()
        for trait_body in utterance_json[Utterance.TRAITS.value]:
            if not self.data.get(trait_body[UtteranceTrait.TRAIT.value]):
                self._append_trait_from_utterance(trait_body=trait_body)
            else:
                self._append_value_from_utterance(trait_body=trait_body)
        return self.actions.get()

    def _append_trait_from_utterance(self, trait_body: Dict[str, Any]) -> None:
        self.data[trait_body[UtteranceTrait.TRAIT.value]] = {trait_body[TraitValue.VALUE.value]}
        self.actions.append_trait_action(
            trait_name=trait_body[UtteranceTrait.TRAIT.value], values={trait_body[TraitValue.VALUE.value]}
        )

    def _append_value_from_utterance(self, trait_body: Dict[str, Any]) -> None:
        trait_name = trait_body[UtteranceTrait.TRAIT.value]
        value = trait_body[TraitValue.VALUE.value]
        local_values = self.data[trait_name]
        if value not in local_values:
            local_values.add(value)
            self.actions.append_value_action(trait_name=trait_name, value=value)


class LocalTrait(LocalTraitFromTrait, LocalLocalFromUtterance):
    pass
