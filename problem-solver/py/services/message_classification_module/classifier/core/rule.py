"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""


from collections import deque
from typing import Callable, List

from spacy.tokens import Token

from common.sc_log import Log

from message_classification_module.classifier.core.constants.common_constants import POSITION_ANY
from message_classification_module.constants.constants import MODULE_NAME

log = Log(MODULE_NAME)


def merge_sentence_rules(sentence_rules) -> List:
    result = []
    for sentence_rule in sentence_rules:
        if isinstance(sentence_rule, (SentenceRule, SentencePositionRule)):
            result.append(sentence_rule)
        elif isinstance(sentence_rule, list) and all(
            isinstance(rule, (SentenceRule, SentencePositionRule)) for rule in sentence_rule
        ):
            result += sentence_rule
        else:
            raise TypeError(f"the type must be in [SentenceRule, list[SentenceRule]. Got {sentence_rule}")
    return result


class Rule:
    def __call__(self, word: Token) -> bool:
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class SpecWordRule(Rule):
    def __init__(self, word_list: List[str]):
        self.word_list = word_list

    def __call__(self, word: Token) -> bool:
        result = False
        if word.text.lower() in self.word_list:
            result = True
        log.debug(f"Check {self.__str__()}: {result}, got {word.text.lower()}")
        return result

    def __str__(self):
        return f"{self.__class__.__name__}({self.word_list})"


class EndRule(Rule):
    def __init__(self, end_list: List[str]):
        self.end_list = end_list

    def __call__(self, word: Token) -> bool:
        result = False
        for end in self.end_list:
            if word.text[len(word) - len(end) :] == end:
                result = True
                break
        log.debug(f"Check {self.__str__()}: {result}, got {word.text}")
        return result

    def __str__(self):
        return f"{self.__class__.__name__}({self.end_list})"


class PosRule(Rule):
    def __init__(self, pos_list: List[str]):
        self.pos_list = pos_list

    def __call__(self, word: Token) -> bool:

        result = word.pos_ in self.pos_list

        log.debug(f"Check {self.__str__()}: {result}, got '{word.text}' pos={word.pos_}")
        return result

    def __str__(self):
        return f"{self.__class__.__name__}({self.pos_list})"


class TagRule(Rule):
    def __init__(self, tag_list: List[str]):
        self.tag_list = tag_list

    def __call__(self, word: Token) -> bool:
        result = word.tag_ in self.tag_list

        log.debug(f"Check {self.__str__()}: {result}, got '{word.text}' tag={word.tag_}")
        return result

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.tag_list})"


class DepRule(Rule):
    def __init__(self, dep_list: List[str]):
        self.dep_list = dep_list

    def __call__(self, word: Token) -> bool:
        result = False
        if word.dep_ in self.dep_list:
            result = True
        log.debug(f"Check {self.__str__()}: {result}, got '{word.text}' dep={word.dep_}")
        return result

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.dep_list})"


class WordRule(Rule):
    def __init__(self, list_rule: List[Callable]):
        for rule in list_rule:
            if not isinstance(rule, Rule):
                raise TypeError(f"{rule} must be in Rule. Got {type(rule)}")
        self.list_rule = list_rule

    def __call__(self, word: Token) -> bool:
        result = True
        for rule in self.list_rule:
            if not rule(word):
                result = False
                break
        log.debug(f"Check {self.__str__()}: {result}")
        return result

    def __str__(self) -> str:
        result = []
        for rule in self.list_rule:
            result.append(str(rule))
        return f"{self.__class__.__name__}({', '.join(result)})"


class SentenceRule(Rule):
    def __init__(self, list_word_rule: List[WordRule]):
        for rule in list_word_rule:
            if not isinstance(rule, WordRule):
                raise TypeError(f"{rule} must be {WordRule.__class__.__name__}. Got {type(rule)}")
        self.list_word_rule = list_word_rule
        self.deq: deque = deque(maxlen=len(self.list_word_rule))
        self.index_rule = 0

    def __call__(self, sentence: List[Token]) -> bool:
        if len(self.deq) > len(sentence):
            return False

        self.reset_index()
        self.deq.clear()

        result = False
        for word in sentence:
            word_check = self.word_rules(word)
            self.deq.append(word_check)
            if len(self.deq) == self.deq.maxlen and all(self.deq):
                result = True
                break
        log.debug(f"Check {self.__str__()}: {result}")
        return result

    def word_rules(self, word: Token) -> bool:
        result = False
        word_rule = self.list_word_rule[self.index_rule]
        if word_rule(word):
            result = True
            self.increase_index_rule()
        else:
            if self.index_rule > 0:
                self.reset_index()
                return self.word_rules(word)
        return result

    def increase_index_rule(self) -> None:
        self.index_rule += 1

    def reset_index(self) -> None:
        self.index_rule = 0

    def __str__(self) -> str:
        result = []
        for rule in self.list_word_rule:
            result.append(str(rule))
        return f"{self.__class__.__name__}({', '.join(result)})"


class SentencePositionRule(Rule):
    def __init__(self, list_word_rule: List[WordRule], list_word_position: List):
        self.list_word_rule = list_word_rule
        self.list_word_position = list_word_position
        self.index_position = 0
        self.index_rule = 0
        self.deq: deque = deque(maxlen=len(self.list_word_rule))

    def word_position(self, word: Token, sentence: List[Token], word_position) -> bool:
        if word_position == POSITION_ANY:
            self.increase_index_position()
            result = True
        elif abs(word_position) <= len(sentence) and sentence[word_position].text == word.text:
            self.increase_index_position()
            result = True
        else:
            self.reset_index()
            result = False
        return result

    def word_rules(self, word: Token, word_position: int) -> bool:
        result = False
        word_rule = self.list_word_rule[self.index_rule]
        if word_rule(word):
            result = True
            self.increase_index_rule()
        else:
            if word_position != POSITION_ANY:
                if self.index_rule > 0:
                    self.reset_index()
                    return self.word_rules(word, word_position)

                self.reset_index()

        return result

    def __call__(self, sentence: List[Token]) -> bool:
        if len(self.deq) > len(sentence):
            return False

        self.reset_index()
        self.deq.clear()

        result = False
        for word in sentence:
            word_position = self.list_word_position[self.index_position]
            if self.word_rules(word, word_position):
                if self.word_position(word, sentence, word_position):
                    self.deq.append(True)
            elif word_position == POSITION_ANY:
                continue
            else:
                self.deq.append(False)
            if len(self.deq) == self.deq.maxlen and all(self.deq):
                result = True
                break
        log.debug(f"Check {self.__str__()}: {result}")
        return result

    def reset_index(self) -> None:
        self.index_rule = 0
        self.index_position = 0

    def increase_index_rule(self) -> None:
        self.index_rule += 1

    def increase_index_position(self) -> None:
        self.index_position += 1

    def __str__(self) -> str:
        result = []
        for rule in self.list_word_rule:
            result.append(str(rule))
        return f"{self.__class__.__name__}({', '.join(result)}, Positions={self.list_word_position})"
