"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""

from typing import Dict, List, Set

from message_classification_module.classifier.task.english_sentence_topic.core.constants.constants import (
    Entity,
    EntityAction,
    EntityKeywords,
    EntitySynonym,
    IntentAction,
    Trait,
    TraitAction,
    TraitValue,
)

from message_classification_module.classifier.task.english_sentence_topic.core.utils import is_built_in


class WitIntentAction:
    def __init__(self):
        self.actions = {IntentAction.ADD_INTENT.value: ""}

    def set_intent_action(self, intent_name: str) -> None:
        self.actions[IntentAction.ADD_INTENT.value] = intent_name

    def clear(self) -> None:
        self.actions[IntentAction.ADD_INTENT.value] = ""

    def get(self) -> Dict[str, str]:
        return self.actions


class WitEntityAction:
    def __init__(self):
        self.actions = {
            EntityAction.ADD_ENTITY.value: list(),
            EntityAction.ADD_ROLES.value: list(),
            EntityAction.ADD_KEYWORDS.value: list(),
            EntityAction.ADD_SYNONYMS.value: list(),
        }

    def append_entity_action(self, entity_name: str, roles: Set[str], keywords: Dict[str, Set[str]]):
        keywords_prep = list()
        for keyword_name, synonyms in keywords.items():
            keywords_prep.append(
                {EntityKeywords.KEYWORD.value: keyword_name, EntityKeywords.SYNONYMS.value: list(synonyms)}
            )
        self.actions[EntityAction.ADD_ENTITY.value].append(
            {Entity.NAME.value: entity_name, Entity.ROLES.value: list(roles), Entity.KEYWORDS.value: keywords_prep}
        )

    def append_role_action(self, entity_name: str, role: str):
        """
        An exception to the rule: to add a new role using WitApi, you need to send a GET entity,
        then add a new role into the list of roles, then send POST to update the entity
        :param entity_name:
        :param role:
        :return:
        """
        if not is_built_in(value=entity_name):
            self.actions[EntityAction.ADD_ROLES.value].append(
                {Entity.NAME.value: entity_name, Entity.ROLES.value: [role]}
            )

    def append_keyword_action(self, entity_name: str, keyword_name: str, synonyms: List[str]):
        """

        :param entity_name:
        :param keyword_name:
        :param synonyms:
        :return:
        Result example:
        {
            "name": "entity_name",
            "keyword_name": "keyword_name",
            "synonyms": ["keyword_name", "synonym_1"]
        }
        """
        if not is_built_in(value=entity_name):
            self.actions[EntityAction.ADD_KEYWORDS.value].append(
                {
                    Entity.NAME.value: entity_name,
                    EntityKeywords.KEYWORD.value: keyword_name,
                    EntityKeywords.SYNONYMS.value: synonyms,
                }
            )

    def append_synonym_action(self, entity_name: str, keyword_name: str, synonym: str):
        if not is_built_in(value=entity_name):
            self.actions[EntityAction.ADD_SYNONYMS.value].append(
                {
                    Entity.NAME.value: entity_name,
                    EntitySynonym.KEYWORD.value: keyword_name,
                    EntitySynonym.SYNONYM.value: synonym,
                }
            )

    def clear(self):
        self.actions[EntityAction.ADD_ENTITY.value].clear()
        self.actions[EntityAction.ADD_ROLES.value].clear()
        self.actions[EntityAction.ADD_KEYWORDS.value].clear()
        self.actions[EntityAction.ADD_SYNONYMS.value].clear()

    def get(self):
        return self.actions


class WitTraitAction:
    def __init__(self):
        self.actions = {TraitAction.ADD_TRAIT.value: list(), TraitAction.ADD_VALUES.value: list()}

    def append_trait_action(self, trait_name: str, values: Set[str]):
        if not is_built_in(trait_name):
            self.actions[TraitAction.ADD_TRAIT.value].append(
                {Trait.NAME.value: trait_name, TraitValue.VALUE.value: list(values)}
            )

    def append_value_action(self, trait_name: str, value: str):
        if not is_built_in(value=trait_name):
            self.actions[TraitAction.ADD_VALUES.value].append(
                {Trait.NAME.value: trait_name, TraitValue.VALUE.value: value}
            )

    def clear(self):
        self.actions[TraitAction.ADD_TRAIT.value].clear()
        self.actions[TraitAction.ADD_VALUES.value].clear()

    def get(self):
        return self.actions
