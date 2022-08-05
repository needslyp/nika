"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""

import json
from typing import Any, Dict, List

import requests

from common.sc_log import Log
from message_classification_module.classifier.task.english_sentence_topic.core.constants.constants import (
    Entity,
    EntityKeywords,
    EntitySynonym,
    Headers,
    Intent,
    Trait,
    Utterance,
)


class WitHeaders:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def authorization(self):
        return {Headers.AUTHORIZATION.value: f"Bearer {self.access_token}"}

    def content_type(self):
        return {Headers.CONTENT_TYPE.value: "application/json"}

    def compose(self, headers: List[Dict[str, str]]):
        result = dict()
        for header in headers:
            result.update(header)
        return result


class WitAPI:  # pylint: disable=R0904
    def __init__(
        self,
        access_token: str,
        wit_api_host: str = "https://api.wit.ai",
        wit_api_version: str = "20200513",
        reply: int = 5,
    ):
        self.access_token = access_token
        self.wit_api_host = wit_api_host
        self.wit_api_version = wit_api_version
        self.reply = reply
        self.wit_headers = WitHeaders(access_token=access_token)
        self.log = Log(self.__class__.__name__)

    def get_message(self, message: str, context=None, n=None, verbose=None):
        params = dict()
        if n is not None:
            params["n"] = n
        if message:
            params["q"] = message
        if context is not None:
            params["context"] = json.dumps(context)
        if verbose is not None:
            params["verbose"] = verbose
        return self._wit_request(
            method="GET", url=self._wit_url("message"), headers=self.wit_headers.authorization(), params=params
        )

    def get_intents(self):
        return self._wit_request(method="GET", url=self._wit_url("intents"), headers=self.wit_headers.authorization())

    def get_intent(self, intent_name: str):
        return self._wit_request(
            method="GET", url=self._wit_url(f"intents/{intent_name}"), headers=self.wit_headers.authorization()
        )

    def add_intent(self, intent_name: str):
        return self._wit_request(
            method="POST",
            url=self._wit_url("intents"),
            headers=self.wit_headers.compose([self.wit_headers.authorization(), self.wit_headers.content_type()]),
            json_data={Intent.NAME.value: intent_name},
        )

    def delete_intent(self, intent_name: str):
        return self._wit_request(
            method="DELETE",
            url=self._wit_url(f"intents/{intent_name}"),
            headers=self.wit_headers.compose([self.wit_headers.authorization(), self.wit_headers.content_type()]),
        )

    def get_entities(self):
        return self._wit_request(method="GET", url=self._wit_url("entities"), headers=self.wit_headers.authorization())

    def get_entity(self, entity_name: str):
        return self._wit_request(
            method="GET", url=self._wit_url(f"entities/{entity_name}"), headers=self.wit_headers.authorization()
        )

    def add_entity(
        self, entity_name: str, roles: List[str] = None, lookups: List[str] = None, keywords: List[str] = None
    ):
        """
        :param entity_name: new entity value
        :param roles: the default role is the value of the entity
        :param lookups: a [free text], [keywords] or both can be if it's empty
        :param keywords: [{'keyword': keyword_1, 'synonyms': [keyword_1, synonym_1, ... , synonym_n]}]
        :return: response in the json format
        """
        return self._wit_request(
            method="POST",
            url=self._wit_url("entities"),
            headers=self.wit_headers.compose([self.wit_headers.authorization(), self.wit_headers.content_type()]),
            json_data={
                Entity.NAME.value: entity_name,
                Entity.ROLES.value: roles if roles is not None else [entity_name],
                Entity.LOOKUPS.value: lookups if lookups is not None else [],
                Entity.KEYWORDS.value: keywords if keywords is not None else [],
            },
        )

    def update_entity(
        self, entity_name: str, roles: List[str] = None, lookups: List[str] = None, keywords: List[str] = None
    ):
        return self._wit_request(
            method="PUT",
            url=self._wit_url(f"entities/{entity_name}"),
            headers=self.wit_headers.compose([self.wit_headers.authorization(), self.wit_headers.content_type()]),
            json_data={
                Entity.NAME.value: entity_name,
                Entity.ROLES.value: roles,
                Entity.LOOKUPS.value: lookups,
                Entity.KEYWORDS.value: keywords,
            },
        )

    def add_entity_keyword(self, entity_name: str, keyword_name: str, synonyms: List[str]):
        if len(keyword_name) > 280:
            raise AttributeError(f"The length of the keyword must be less than 280 characters. Got {len(keyword_name)}")
        return self._wit_request(
            method="POST",
            url=self._wit_url(f"entities/{entity_name}/keywords"),
            headers=self.wit_headers.compose([self.wit_headers.authorization(), self.wit_headers.content_type()]),
            json_data={EntityKeywords.KEYWORD.value: keyword_name, EntityKeywords.SYNONYMS.value: synonyms},
        )

    def add_entity_synonym(self, entity_name: str, keyword_name: str, synonym: str):
        if len(synonym) > 280:
            raise AttributeError(f"The length of the synonym must be less than 280 characters. Got {len(synonym)}")
        return self._wit_request(
            method="POST",
            url=self._wit_url(f"entities/{entity_name}/keywords/{keyword_name}/synonyms"),
            headers=self.wit_headers.compose([self.wit_headers.authorization(), self.wit_headers.content_type()]),
            json_data={EntitySynonym.SYNONYM.value: synonym},
        )

    def delete_entity_synonym(self, entity_name: str, keyword_name: str, synonym_name: str):
        return self._wit_request(
            method="DELETE",
            url=self._wit_url(f"entities/{entity_name}/keywords/{keyword_name}/synonyms/{synonym_name}"),
            headers=self.wit_headers.authorization(),
        )

    def delete_entity(self, entity_name: str):
        return self._wit_request(
            method="DELETE", url=self._wit_url(f"entities/{entity_name}"), headers=self.wit_headers.authorization()
        )

    def get_traits(self):
        return self._wit_request(method="GET", url=self._wit_url("traits"), headers=self.wit_headers.authorization())

    def get_trait(self, trait_name: str):
        return self._wit_request(
            method="GET", url=self._wit_url(f"traits/{trait_name}"), headers=self.wit_headers.authorization()
        )

    def add_trait(self, trait_name: str, values: List[str]):
        return self._wit_request(
            method="POST",
            url=self._wit_url("traits"),
            headers=self.wit_headers.compose([self.wit_headers.authorization(), self.wit_headers.content_type()]),
            json_data={Trait.NAME.value: trait_name, Trait.VALUES.value: values},
        )

    def add_trait_value(self, trait_name: str, value: str):
        return self._wit_request(
            method="POST",
            url=self._wit_url(f"traits/{trait_name}/values"),
            headers=self.wit_headers.compose([self.wit_headers.authorization(), self.wit_headers.content_type()]),
            json_data={"value": value},
        )

    def delete_trait_value(self, trait_name: str, value: str):
        return self._wit_request(
            method="DELETE",
            url=self._wit_url(f"traits/{trait_name}/values/{value}"),
            headers=self.wit_headers.authorization(),
        )

    def delete_trait(self, trait_name: str) -> Dict[str, Any]:
        return self._wit_request(
            method="DELETE", url=self._wit_url(f"traits/{trait_name}"), headers=self.wit_headers.authorization()
        )

    def get_utterances(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._wit_request(
            method="GET", url=f"{self._wit_url('utterances')}&limit={limit}", headers=self.wit_headers.authorization()
        )

    def add_utterance(
        self, text: str, intent_name: str, entities: List[Dict[str, str]] = None, traits: List[Dict[str, str]] = None
    ):
        return self._wit_request(
            method="POST",
            url=self._wit_url("utterances"),
            headers=self.wit_headers.compose([self.wit_headers.authorization(), self.wit_headers.content_type()]),
            json_data=[
                {
                    Utterance.TEXT.value: text,
                    Utterance.INTENT.value: intent_name,
                    Utterance.ENTITIES.value: entities if entities is not None else [],
                    Utterance.TRAITS.value: traits if traits is not None else [],
                }
            ],
        )

    def add_utterance_json(self, utterance_json: List[Dict[str, Any]]):
        return self._wit_request(
            method="POST",
            url=self._wit_url("utterances"),
            headers=self.wit_headers.compose([self.wit_headers.authorization(), self.wit_headers.content_type()]),
            json_data=utterance_json,
        )

    def delete_utterance(self, text: str):
        return self._wit_request(
            method="DELETE",
            url=self._wit_url("utterances"),
            headers=self.wit_headers.compose([self.wit_headers.authorization(), self.wit_headers.content_type()]),
            json_data=[{Utterance.TEXT.value: text}],
        )

    def _wit_request(self, method: str, url: str, headers: Dict[str, str], json_data=None, params=None):
        self.log.debug(
            f"Send request: method={method}, url={url}, headers={headers}, json={json_data}, params={params}"
        )
        response = None
        reply = self.reply
        while reply > 0:
            response = requests.request(method=method, url=url, headers=headers, json=json_data, params=params)
            if response.status_code == 200:
                reply = 0
            else:
                reply -= 1
        self.log.debug(f"Get response={response}")
        return self._wit_response(response)

    def _wit_url(self, body: str):
        return f"{self.wit_api_host}/{body}?v={self.wit_api_version}"

    def _wit_response(self, response):
        if response.status_code == 200:
            result = response.json()
        else:
            result = f"Response status_code <{response.status_code}>: {response.reason}"
        return result
