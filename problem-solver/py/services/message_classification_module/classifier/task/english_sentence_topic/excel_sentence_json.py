"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""

from typing import Any, Dict, List

from message_classification_module.classifier.task.english_sentence_topic.core.constants.constants import (
    EntityKeywords,
    Utterance,
    UtteranceEntity,
    UtteranceTrait,
)


class WitUtteranceJson:
    def __init__(self):
        self.result = {
            Utterance.TEXT.value: "",
            Utterance.INTENT.value: "",
            Utterance.ENTITIES.value: [],
            Utterance.TRAITS.value: [],
        }

    def set_text(self, text: str) -> None:
        self.result[Utterance.TEXT.value] = text

    def set_intent(self, intent_name: str) -> None:
        self.result[Utterance.INTENT.value] = intent_name

    def append_entity(self, entity_name: str, role: str = None, keywords: List[Dict[str, Any]] = None) -> None:
        if entity_name.startswith("wit$"):
            role = entity_name[4:] if role is None else role
        else:
            role = entity_name if role is None else role
        for keyword in keywords:
            body = keyword[EntityKeywords.KEYWORD.value]
            entity_start = self.result[Utterance.TEXT.value].find(body)
            entity_end = entity_start + len(body)
            self.result[Utterance.ENTITIES.value].append(
                {
                    UtteranceEntity.ENTITY.value: f"{entity_name}:{role}",
                    UtteranceEntity.START.value: entity_start,
                    UtteranceEntity.END.value: entity_end,
                    UtteranceEntity.BODY.value: body,
                    UtteranceEntity.ENTITIES.value: [],
                }
            )

    def append_trait(self, trait_name: str, value: str) -> None:
        self.result[Utterance.TRAITS.value].append(
            {UtteranceTrait.TRAIT.value: trait_name, UtteranceTrait.VALUE.value: value}
        )

    def get(self):
        return self.result
