"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""


from typing import List, Tuple

import spacy
from spacy.tokens import Span, Token

from common.sc_log import Log

from message_classification_module.classifier.core.constants import spacy_constants as sc
from message_classification_module.classifier.core.filter import Filter
from message_classification_module.classifier.core.sentence_part import SentencePart
from message_classification_module.constants.constants import MODULE_NAME

log = Log(MODULE_NAME)
nlp = spacy.load(sc.EN_CORE_WEB_MD)

FILTER_TAG = "filter_tag"
FILTER_POS = "filter_pos"
FILTER_SYMBOLS = "filter_symbols"


class TextPreprocess:
    def __init__(
        self,
        list_filter_word: List[Filter] = None,
        symbol_replace: List[Tuple[str, str]] = None,
        find_sentence_part: bool = False,
    ):
        """
        :param tag_filter: list nlp tags that won't be filtered
        :param pos_filter: list nlp pos that won't be filtered
        :param symbols: list of the tuple symbols (from, to) for replacing
        :param find_sentence_part: separating every sentence by predicate count in sentence
        """
        self.list_filter_word = list_filter_word if list_filter_word is not None else list()
        self.symbol_replace = symbol_replace if symbol_replace is not None else list()
        self.sentence_part = SentencePart() if find_sentence_part else None
        self.process_compose = self.set_process_compose()

    def set_process_compose(self):
        compose = list()
        if len(self.symbol_replace) != 0:
            compose.append(self.replace_symbols)
        compose.append(self.text_to_sentences)
        if len(self.list_filter_word) != 0:
            compose.append(self.filter)
        if isinstance(self.sentence_part, SentencePart):
            compose.append(self.sentence_part)
        return compose

    def process(self, text: str):
        for fn in self.process_compose:
            text = fn(text)
        return text

    def replace_symbols(self, text: str) -> str:
        for (symbol_from, symbol_to) in self.symbol_replace:
            text = text.replace(symbol_from, symbol_to)
        log.debug(f"After the replaced symbols {self.symbol_replace}: '{text}'")
        return text

    def filter_sentence(self, sentence) -> List[Token]:
        result = []
        for word in sentence:
            append = True
            if self.list_filter_word is not None:
                for filter_word in self.list_filter_word:
                    if not filter_word(word):
                        append = False
                        break
            if append:
                result.append(word)
        return result

    def filter(self, sentences: List[Span]) -> List[List[Token]]:
        result = list()
        for sentence in sentences:
            result.append(self.filter_sentence(sentence))
        return result

    @staticmethod
    def text_to_sentences(text: str) -> List[Span]:
        return list(nlp(text).sents)

    def __call__(self, text: str) -> List[List[Token]]:
        log.debug(f"Get a text '{text}'")
        result = self.process(text)
        log.debug(f"After filtering the sentence: {result}")
        return result
