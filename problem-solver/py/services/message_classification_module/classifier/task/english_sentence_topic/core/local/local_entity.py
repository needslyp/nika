"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""

from typing import Any, Dict, List, Set

from message_classification_module.classifier.task.english_sentence_topic.core.constants.constants import (
    Entity,
    EntityKeywords,
    EntityRoles,
    UtteranceEntity,
)
from message_classification_module.classifier.task.english_sentence_topic.core.local.local_data import LocalData
from message_classification_module.classifier.task.english_sentence_topic.core.wit_action import WitEntityAction


class LocalEntityFromEntity(LocalData):
    def append_from_entity(self, entity_json: Dict[str, Any]):
        """
        No actions
        :param entity_json:
        :return: action if action, else empty dict

        Example:
        {
            "id": 777,
            "name": "entity_name",
            "lookups": ["keywords", "free-text"],
            "roles": ["entity_name"],
            "keywords": [
                {
                    "keyword": "key_name_1",
                    "synonyms": ["key_name_1", "key_syn_name_1"]
                }
            ]
        }
        """
        entity_name = entity_json[Entity.NAME.value]
        if not self.data.get(entity_name, False):
            self.data[entity_name] = dict()
            self._create_roles_from_entity(entity_name=entity_name, roles=entity_json[Entity.ROLES.value])
            self._create_keywords_from_entity(
                entity_name=entity_name, keywords=entity_json.get(Entity.KEYWORDS.value, list())
            )
        else:
            self._append_roles_from_entity(entity_name=entity_name, roles=entity_json[Entity.ROLES.value])
            self._append_keywords_from_entity(entity_name=entity_name, keywords=entity_json[Entity.KEYWORDS.value])

    def _create_roles_from_entity(self, entity_name: str, roles: List[str]):
        result = set()
        for role in roles:
            result.add(role[EntityRoles.NAME.value])
        self.data[entity_name][Entity.ROLES.value] = result

    def _create_keywords_from_entity(self, entity_name: str, keywords: List[Dict[str, Any]]):
        result = dict()
        for keyword in keywords:
            result[keyword[EntityKeywords.KEYWORD.value]] = set(keyword[EntityKeywords.SYNONYMS.value])
        self.data[entity_name][Entity.KEYWORDS.value] = result

    def _append_roles_from_entity(self, entity_name: str, roles: List[str]):
        local_roles = self.data[entity_name][Entity.ROLES.value]
        for role in roles:
            if role not in local_roles:
                local_roles.add(role)

    def _append_keywords_from_entity(self, entity_name: str, keywords: List[Dict[str, Any]]):
        locale_keywords = self.data[entity_name][Entity.KEYWORDS.value]
        for keyword in keywords:
            keyword_name = keyword[EntityKeywords.KEYWORD.value]
            if not locale_keywords.get(keyword_name, False):
                synonyms = keyword[EntityKeywords.SYNONYMS.value]
                locale_keywords[keyword[EntityKeywords.KEYWORD.value]] = set(synonyms)
            else:
                self._append_keyword_synonyms_from_entity(
                    locale_synonyms=locale_keywords[keyword_name], synonyms=keyword[EntityKeywords.SYNONYMS.value]
                )

    @staticmethod
    def _append_keyword_synonyms_from_entity(locale_synonyms: Set[str], synonyms: List[str]):
        for synonym in synonyms:
            if synonym not in locale_synonyms:
                locale_synonyms.add(synonym)


class LocalLocalFromUtterance(LocalData):
    def __init__(self):
        """
        Set a local entity from wit.ai utterance json response
        """
        super().__init__()
        self.actions = WitEntityAction()

    @staticmethod
    def _utterance_json_preprocessing(utterance_json: Dict[str, Any]) -> Dict[str, Any]:
        result = dict()
        for entity in utterance_json[UtteranceEntity.ENTITIES.value]:
            entity_name, _ = entity[UtteranceEntity.ENTITY.value].split(":")
            if not result.get(entity_name, False):
                result[entity_name] = [entity]
            else:
                result[entity_name].append(entity)
        return result

    def append_from_utterance(self, utterance_json: Dict[str, Any]):
        """
        :param utterance_json:
        :return: action if action, else empty dict

        Example of wit_utterance_response:
        {
            "text": "text example",
            "entities": [
                {
                    "entity": "entity_name:entity_role",
                    "start": 5,
                    "end": 12,
                    "body": "example",
                    "entities": []
                }
            ]
        }
        """
        self.actions.clear()
        entities = self._utterance_json_preprocessing(utterance_json)
        for entity_name, entity_bodies in entities.items():
            if not self.data.get(entity_name, False):
                self._append_entity_from_utterance(entity_name=entity_name, entity_bodies=entity_bodies)
            else:
                self._append_entity_context_from_utterance(entity_name=entity_name, entity_bodies=entity_bodies)
        return self.actions.get()

    def _append_entity_from_utterance(self, entity_name: str, entity_bodies: List[Dict[str, Any]]):
        self.data[entity_name] = dict()
        self.data[entity_name][Entity.ROLES.value] = set()
        self.data[entity_name][Entity.KEYWORDS.value] = dict()
        for entity_body in entity_bodies:
            _, role = entity_body[UtteranceEntity.ENTITY.value].split(":")
            keyword_name = entity_body[UtteranceEntity.BODY.value]
            self.data[entity_name][Entity.ROLES.value].add(role)
            self.data[entity_name][Entity.KEYWORDS.value][keyword_name] = {keyword_name}
        self.actions.append_entity_action(
            entity_name=entity_name,
            roles=self.data[entity_name][Entity.ROLES.value],
            keywords=self.data[entity_name][Entity.KEYWORDS.value],
        )

    def _append_entity_context_from_utterance(self, entity_name: str, entity_bodies: List[Dict[str, Any]]):
        local_roles = self.data[entity_name][Entity.ROLES.value]
        locale_keywords = self.data[entity_name][Entity.KEYWORDS.value]
        for entity_body in entity_bodies:
            self._append_role_from_utterance(local_roles=local_roles, entity_body=entity_body)
            self._append_keywords_from_utterance(local_keywords=locale_keywords, entity_body=entity_body)

    def _append_role_from_utterance(self, local_roles: Set[str], entity_body: Dict[str, Any]):
        entity_name, role = entity_body[UtteranceEntity.ENTITY.value].split(":")
        if role not in local_roles:
            local_roles.add(role)
            self.actions.append_role_action(entity_name=entity_name, role=role)

    def _append_keywords_from_utterance(self, local_keywords: Dict[str, Any], entity_body: Dict[str, Any]):
        entity_name, _ = entity_body[UtteranceEntity.ENTITY.value].split(":")
        if not local_keywords.get(entity_body[UtteranceEntity.BODY.value], False):
            self.actions.append_keyword_action(
                entity_name=entity_name,
                keyword_name=entity_body[UtteranceEntity.BODY.value],
                synonyms=entity_body[UtteranceEntity.BODY.value],
            )


class LocalEntityEntityFromEntity(LocalEntityFromEntity, LocalLocalFromUtterance):
    pass
