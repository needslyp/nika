"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""

from typing import Any, Callable, Dict, List, Set
from common.sc_log import Log

import pandas as pd

from message_classification_module.classifier.core.utils.average import Average
from message_classification_module.classifier.task.english_sentence_topic.core.constants.constants import (
    EntityKeywords,
    Utterance,
)
from message_classification_module.classifier.task.english_sentence_topic.core.utils import is_built_in
from message_classification_module.classifier.task.english_sentence_topic.core.wit_api_trainer import (
    WitApiTrainer,
)
from message_classification_module.classifier.task.english_sentence_topic.excel_sentence_json import (
    WitUtteranceJson,
)


EXAMPLE = "example"
INTENT = "intent"
ENTITY = "entity"
TRAIT = "trait"


def get_clear_column_name(column_name: str) -> str:
    return column_name[2:]


def is_text(value: str) -> bool:
    return value == "example"


def is_intent(value: str) -> bool:
    return value[0] == "i"


def is_entity(value: str) -> bool:
    return value[0] == "e"


def is_trait(value: str) -> bool:
    return value[0] == "t"


class WitAiBuiltInChecker:
    def __init__(self, wit_api_trainer: WitApiTrainer):
        self.wit_api_trainer = wit_api_trainer
        self.INTENTS = "intents"
        self.TRAITS = "traits"
        self.ENTITIES = "entities"

    def __call__(self, df: pd.DataFrame) -> Dict[str, Set[str]]:
        old_built_in = self.current_built_in()
        new_built_in = self.excel_built_in(df)
        result = {self.INTENTS: set(), self.ENTITIES: set(), self.TRAITS: set()}
        for key, values in new_built_in.items():
            for value in values:
                if value not in old_built_in[key]:
                    result[key].add(value)
        return result

    def check_built_in(self, df: pd.DataFrame) -> Set[str]:
        pass

    def current_built_in(self) -> Dict[str, Set[str]]:
        return {
            "intents": self._current_built_in_items(items=self.wit_api_trainer.intents()),
            "entities": self._current_built_in_items(items=self.wit_api_trainer.entities()),
            "traits": self._current_built_in_items(items=self.wit_api_trainer.traits()),
        }

    def _current_built_in_items(self, items: List[str]):
        result = set()
        for item in items:
            if is_built_in(item):
                result.add(item)
        return result

    def excel_built_in(self, df: pd.DataFrame) -> Dict[str, Set[str]]:
        result = {self.INTENTS: set(), self.ENTITIES: set(), self.TRAITS: set()}
        for sheet_name in df.sheet_names:
            df_sheet = df.parse(sheet_name)
            for column_name in list(df_sheet):
                if self._excel_built_in(column_name=column_name, main_check_fn=is_intent):
                    result[self.INTENTS].add(get_clear_column_name(column_name))
                elif self._excel_built_in(column_name=column_name, main_check_fn=is_entity):
                    result[self.ENTITIES].add(get_clear_column_name(column_name))
                elif self._excel_built_in(column_name=column_name, main_check_fn=is_trait):
                    result[self.TRAITS].add(get_clear_column_name(column_name))
        return result

    def _excel_built_in(self, column_name: str, main_check_fn: Callable) -> bool:
        result = False
        if main_check_fn(column_name):
            intent_name = get_clear_column_name(column_name)
            if is_built_in(intent_name):
                result = True
        return result


class ExcelTopic:
    def __init__(self, wit_api_trainer: WitApiTrainer):
        self.wit_api_trainer = wit_api_trainer
        self.wit_ai_built_in_checker = WitAiBuiltInChecker(self.wit_api_trainer)
        self.acc = Average()
        self.fail_count = 0
        self.log = Log(self.__class__.__name__)

    @staticmethod
    def next_sentence(df: pd.DataFrame):
        for _, row in df.iterrows():
            yield row

    def __call__(self, path: str, mode: str = "test") -> List[Dict[str, List[str]]]:
        checker_map = {"test": self.test, "train": self.train}
        checker = checker_map.get(mode, None)
        if checker is None:
            raise AttributeError(f"mode {mode} is not found in {checker_map.keys()}")
        df = pd.ExcelFile(path)
        return checker(df=df)

    def check_built_in(self, df: pd.DataFrame) -> bool:
        new_built_in = self.wit_ai_built_in_checker(df)
        result = False
        for key, values in new_built_in.items():
            if len(values) > 0:
                if not result:
                    result = True
                    self.log.info("Built-in values are found. Add them to 'wit.ai' before training your application")
                for i, value in enumerate(values, start=1):
                    self.log.info(f"{key}-{i}: {value}")
        return result

    def train(self, df: pd.DataFrame) -> List[Dict[str, List[str]]]:
        result = []
        if not self.check_built_in(df):
            i = -1
            sentence_process = 1
            total_sentence_count = 0
            for sheet_name in df.sheet_names:
                if sheet_name not in ["base"]:
                    total_sentence_count += df.parse(sheet_name).shape[0]
            for sheet_name in df.sheet_names:
                if sheet_name not in ["base"]:
                    df_sheet = df.parse(sheet_name)
                    result.append({sheet_name: list()})
                    i += 1
                    for row in self.next_sentence(df_sheet):
                        wit_utterance_json = WitUtteranceJson()
                        column_keys = self.parse_row(row)
                        for column_key in column_keys:
                            self.process_column_value(
                                wit_utterance_json=wit_utterance_json,
                                column_key=column_key,
                                column_value=row.loc[column_key],
                            )
                        utterance_json = wit_utterance_json.get()
                        if utterance_json[Utterance.TEXT.value] != "" and utterance_json[Utterance.INTENT.value] != "":
                            if self.wit_api_trainer.train(utterance_json=utterance_json):
                                self.log.debug(
                                    f"{sentence_process}/{total_sentence_count}: Trained text="
                                    f"'{utterance_json[Utterance.TEXT.value]}' (sheet_name={sheet_name})"
                                )
                            else:
                                self.log.debug(
                                    f"{sentence_process}/{total_sentence_count}: False trained text="
                                    f"'{utterance_json[Utterance.TEXT.value]}' (sheet_name={sheet_name})"
                                )
                                result[i][sheet_name].append(utterance_json[Utterance.TEXT.value])
                            sentence_process += 1
        return result

    def test(self, df: pd.DataFrame) -> List[str]:
        pass

    def process_column_value(
        self, wit_utterance_json: WitUtteranceJson, column_key: str, column_value: str
    ) -> [str, Dict[str, Any]]:
        if is_text(column_key):
            self.set_text(wit_utterance_json=wit_utterance_json, text=column_value)
        elif is_intent(column_key):
            self.set_intent(wit_utterance_json=wit_utterance_json, intent_name=get_clear_column_name(column_key))
        elif is_entity(column_key):
            self.append_entity(
                wit_utterance_json=wit_utterance_json,
                entity_name=get_clear_column_name(column_key),
                keywords_str=column_value,
            )
        elif is_trait(column_key):
            self.append_trait(
                wit_utterance_json=wit_utterance_json, trait_name=get_clear_column_name(column_key), value=column_value
            )
        return wit_utterance_json

    @staticmethod
    def set_text(wit_utterance_json: WitUtteranceJson, text: str):
        wit_utterance_json.set_text(text)

    @staticmethod
    def set_intent(wit_utterance_json: WitUtteranceJson, intent_name: str):
        wit_utterance_json.set_intent(intent_name=intent_name)

    @staticmethod
    def remove_left_space(value: str):
        index = 0
        flag = True
        while flag:
            if value[index] == " ":
                index += 1
            else:
                flag = False
        return value[index:]

    @staticmethod
    def remove_right_space(value: str):
        index = len(value) - 1
        flag = True
        while flag:
            if value[index] == " ":
                index -= 1
            else:
                flag = False
        return value[: index + 1]

    def remove_left_right_space(self, values: List[str]):
        result = []
        for value in values:
            value = self.remove_left_space(value)
            value = self.remove_right_space(value)
            result.append(value)
        return result

    def append_entity(self, wit_utterance_json: WitUtteranceJson, entity_name: str, keywords_str: str):
        keywords_list = self.remove_left_right_space(keywords_str.split(","))
        keywords = list()
        for keyword_name in keywords_list:
            keywords.append({EntityKeywords.KEYWORD.value: keyword_name, EntityKeywords.SYNONYMS.value: [keyword_name]})
        wit_utterance_json.append_entity(entity_name=entity_name, keywords=keywords)

    @staticmethod
    def append_trait(wit_utterance_json: WitUtteranceJson, trait_name: str, value: str):
        wit_utterance_json.append_trait(trait_name=trait_name, value=value)

    @staticmethod
    def parse_row(row: pd.Series) -> List[str]:
        """
        :param row: excel row
        :return: not NaN column keys
        """
        return list(row[row.notna()].copy().keys())
