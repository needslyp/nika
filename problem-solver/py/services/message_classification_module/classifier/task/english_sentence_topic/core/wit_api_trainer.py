"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""

from typing import Any, Dict, List

from common.sc_log import Log
from message_classification_module.classifier.task.english_sentence_topic.core.local.local_data import LocalData

from message_classification_module.classifier.task.english_sentence_topic.core.constants.constants import (
    Entity,
    EntityAction,
    EntityKeywords,
    EntitySynonym,
    Intent,
    IntentAction,
    Trait,
    TraitAction,
    TraitValue,
    Utterance,
)
from message_classification_module.classifier.task.english_sentence_topic.core.wit_api import WitAPI


class WitApiTrainer:
    def __init__(self, wit_api: WitAPI, confidence: int = 0.9, init_local_data=True):
        self.wit_api = wit_api
        self.confidence = confidence
        self.local_data = LocalData()
        self.log = Log(self.__class__.__name__)
        if init_local_data:
            self.set_wit_data_to_local()

    def __call__(self, mode: str, *args, **kwargs):
        checker_map = {"train": self.train, "test": self.test}
        checker = checker_map.get(mode, None)
        if checker is None:
            raise AttributeError(f"mode={mode} is not found in {checker_map.keys()}")
        return checker(kwargs)

    def set_wit_data_to_local(self):
        self._save_intents_local()
        self._save_entities_local()
        self._save_traits_local()

    def _save_intents_local(self):
        self.log.debug("Saving app intents")
        intents = self.wit_api.get_intents()
        for intent in intents:
            self.local_data.append_intent(intent)

    def _save_entities_local(self):
        self.log.debug("Saving app entities")
        entities = self.wit_api.get_entities()
        for entity in entities:
            entity = self.wit_api.get_entity(entity[Entity.NAME.value])
            self.local_data.append_entity(entity)

    def _save_traits_local(self):
        self.log.debug("Saving app traits")
        traits = self.wit_api.get_traits()
        for trait in traits:
            trait = self.wit_api.get_trait(trait[Trait.NAME.value])
            self.local_data.append_trait(trait)

    def _check_response(self, response) -> bool:
        return not isinstance(response, str)

    def _add_intent(self, action: str) -> bool:
        result = False
        if action != "":
            response = self.wit_api.add_intent(action)
            result = self._check_response(response)
            self.log.debug(f"{result} an intent={action} is added")
        return result

    def _add_entities(self, actions: List[Dict[str, Any]]) -> bool:
        result = False
        for action in actions:
            entity_name = action[Entity.NAME.value]
            roles = action[Entity.ROLES.value]
            keywords = action[Entity.KEYWORDS.value]
            response = self.wit_api.add_entity(entity_name=entity_name, roles=roles, keywords=keywords)
            result = self._check_response(response)
            self.log.debug(f"{result} an entity={entity_name}, roles={roles}, keywords={keywords} are added")
        return result

    def _add_entity_roles(self, actions: List[Dict[str, Any]]) -> bool:
        result = False
        for action in actions:
            entity = self.wit_api.get_entity(entity_name=action[Entity.NAME.value])
            if not isinstance(entity, str):
                entity_name = entity[Entity.NAME.value]
                roles = entity[Entity.ROLES.value]
                lookups = entity[Entity.LOOKUPS.value]
                keywords = entity[Entity.KEYWORDS.value]
                response = self.wit_api.update_entity(
                    entity_name=entity_name,
                    roles=entity[Entity.ROLES.value] + roles,
                    lookups=lookups,
                    keywords=keywords,
                )
                result = self._check_response(response)
                self.log.debug(f"{result} entity roles={roles} for the entity={entity_name} are added")
        return result

    def _add_entity_keywords(self, actions: List[Dict[str, Any]]) -> bool:
        result = False
        for action in actions:
            entity_name = action[Entity.NAME.value]
            keyword_name = action[EntitySynonym.KEYWORD.value]
            synonyms = action[EntityKeywords.SYNONYMS.value]
            response = self.wit_api.add_entity_keyword(
                entity_name=entity_name, keyword_name=keyword_name, synonyms=synonyms
            )
            result = self._check_response(response)
            self.log.debug(
                f"{result} an entity keyword={keyword_name} (synonyms={synonyms}) for the entity={entity_name} is added"
            )
        return result

    def _add_entity_synonyms(self, actions: List[Dict[str, Any]]) -> bool:
        result = False
        for action in actions:
            entity_name = action[Entity.NAME.value]
            keyword_name = action[EntitySynonym.KEYWORD.value]
            synonym = action[EntitySynonym.SYNONYM.value]
            response = self.wit_api.add_entity_synonym(
                entity_name=entity_name, keyword_name=keyword_name, synonym=synonym
            )
            result = self._check_response(response)
            self.log.debug(
                f"{result} an entity synonym={synonym} for the keyword={keyword_name} \
                for the entity={entity_name} is added"
            )
        return result

    def _add_traits(self, actions: List[Dict[str, Any]]) -> bool:
        result = False
        for action in actions:
            trait_name = action[Trait.NAME.value]
            values = action[TraitValue.VALUE.value]
            response = self.wit_api.add_trait(trait_name=trait_name, values=values)
            result = self._check_response(response)
            self.log.debug(f"{result} a trait={action[Trait.NAME.value]}, values={values} are added")
        return result

    def _add_trait_values(self, actions: List[Dict[str, Any]]):
        result = False
        for action in actions:
            trait_name = action[Trait.NAME.value]
            value = action[TraitValue.VALUE.value]
            response = self.wit_api.add_trait_value(trait_name=trait_name, value=value)
            result = self._check_response(response)
            self.log.debug(f"{result} a trait value={value} for the trait={trait_name} is added")
        return result

    def _run_intent_action(self, action: Dict[str, str]) -> bool:
        return self._add_intent(action=action[IntentAction.ADD_INTENT.value])

    def _run_entity_action(self, actions: Dict[str, List[Dict[str, Any]]]) -> bool:
        result = self._add_entities(actions=actions[EntityAction.ADD_ENTITY.value])
        result = result or self._add_entity_roles(actions=actions[EntityAction.ADD_ROLES.value])
        result = result or self._add_entity_keywords(actions=actions[EntityAction.ADD_KEYWORDS.value])
        result = result or self._add_entity_synonyms(actions=actions[EntityAction.ADD_SYNONYMS.value])
        return result

    def _run_trait_action(self, actions: Dict[str, Any]) -> bool:
        result = self._add_traits(actions=actions[TraitAction.ADD_TRAIT.value])
        result = result or self._add_trait_values(actions=actions[TraitAction.ADD_VALUES.value])
        return result

    def _run_actions(self, utterance_json: Dict[str, Any]):
        actions = self.local_data(utterance_json)
        self._run_intent_action(action=actions)
        self._run_entity_action(actions=actions)
        self._run_trait_action(actions=actions)

    # TODO add control testing
    def train(self, utterance_json: Dict[str, Any]) -> bool:
        self._run_actions(utterance_json=utterance_json)
        response = self.wit_api.add_utterance_json(utterance_json=[utterance_json])
        return not isinstance(response, str)

    def test(self, text: str):
        return self.wit_api.get_message(message=text)

    def clear_utterances(self):
        utterances_json = [None]
        index = 1
        while isinstance(utterances_json, list) and len(utterances_json) > 0:
            utterances_json = self.wit_api.get_utterances(limit=10)
            if isinstance(utterances_json, list):
                for utterance_json in utterances_json:
                    text = utterance_json[Utterance.TEXT.value]  # pylint: disable=E1136
                    self.log.debug(f"{index}: Deleting the utterance by the text={text}")
                    index += 1
                    if self._check_response(self.wit_api.delete_utterance(text)):
                        self.log.debug("Delete: True")
                    else:
                        self.log.debug("Delete: False")

    def clear_intents(self):
        intents_json = self.wit_api.get_intents()
        for index, intent_json in enumerate(intents_json, start=1):
            intent_name = intent_json[Intent.NAME.value]
            self.log.debug(f"{index}: Deleting the intent by the intent_name={intent_name}")
            response = self.wit_api.delete_intent(intent_name=intent_name)
            if self._check_response(response=response):
                self.log.debug("Delete: True")
            else:
                self.log.debug("Delete: False")

    def clear_entities(self):
        entities_json = self.wit_api.get_entities()
        for index, entity_json in enumerate(entities_json, start=1):
            entity_name = entity_json[Entity.NAME.value]
            self.log.debug(f"{index}: Deleting the entity by the entity_name={entity_name}")
            response = self.wit_api.delete_entity(entity_name=entity_name)
            if self._check_response(response=response):
                self.log.debug("Delete: True")
            else:
                self.log.debug("Delete: False")

    def clear_traits(self):
        traits_json = self.wit_api.get_traits()
        for index, trait_json in enumerate(traits_json, start=1):
            trait_name = trait_json[Trait.NAME.value]
            self.log.debug(f"{index}: Deleting the trait by the trait_name={trait_name}")
            response = self.wit_api.delete_trait(trait_name=trait_name)
            if self._check_response(response=response):
                self.log.debug("Delete: True")
            else:
                self.log.debug("Delete: False")

    def clear(self):
        self.clear_intents()
        self.clear_entities()
        self.clear_traits()
        self.clear_utterances()

    def intents(self):
        response = self.wit_api.get_intents()
        result = []
        if not isinstance(response, str):
            for intent in response:
                result.append(intent[Intent.NAME.value])
        return result

    def entities(self):
        response = self.wit_api.get_entities()
        result = []
        if not isinstance(response, str):
            for entity in response:
                result.append(entity[Entity.NAME.value])
        return result

    def traits(self):
        response = self.wit_api.get_traits()
        result = []
        if not isinstance(response, str):
            for trait in response:
                result.append(trait[Trait.NAME.value])
        return result
