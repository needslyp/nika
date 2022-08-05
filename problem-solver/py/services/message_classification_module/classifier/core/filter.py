"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""


from typing import Callable, List

from spacy.tokens import Token


class FilterCheck:
    def __init__(self, fn_in: Callable[[Token], bool] = None, fn_not_in: Callable[[Token], bool] = None):
        """
        :param fn_in: a function that receives only a word token and checks whether this word is in the filter list by
        condition
        :param fn_not_in: a function that receives only a word token and checks whether this word is not in the filter
        list by condition
        """
        self.fn_in = fn_in if fn_in is not None else lambda word: True
        self.fn_not_in = fn_not_in if fn_not_in is not None else lambda word: True

    def __call__(self, word: Token) -> bool:
        return self.fn_in(word) and self.fn_not_in(word)


class Filter:
    def __init__(self, list_in: List[str] = None, list_not_in: List[str] = None):
        """
        :param list_in: list of the string values that should be
        :param list_not_in: list of the string values that shouldn't be
        """
        self.list_have = list_in
        self.list_not_have = list_not_in
        self.filter_check = FilterCheck(
            fn_in=self.fn_in if self.list_have is not None else None,
            fn_not_in=self.fn_not_in if self.list_not_have is not None else None,
        )

    def fn_in(self, word: Token) -> bool:
        raise NotImplementedError

    def fn_not_in(self, word: Token) -> bool:
        raise NotImplementedError

    def __call__(self, word: Token) -> bool:
        return self.filter_check(word)


class FilterDep(Filter):
    def fn_in(self, word: Token) -> bool:
        if self.list_have is None:
            return False
        return word.dep_ in self.list_have

    def fn_not_in(self, word: Token) -> bool:
        if self.list_not_have is None:
            return False
        return word.dep_ not in self.list_not_have


class FilterTag(Filter):
    def fn_in(self, word: Token) -> bool:
        if self.list_have is None:
            return False
        return word.tag_ in self.list_have

    def fn_not_in(self, word: Token) -> bool:
        if self.list_not_have is None:
            return False
        return word.tag_ not in self.list_not_have


class FilterPos(Filter):
    def fn_in(self, word: Token) -> bool:
        if self.list_have is None:
            return False
        return word.pos_ in self.list_have

    def fn_not_in(self, word: Token) -> bool:
        if self.list_not_have is None:
            return False
        return word.pos_ not in self.list_not_have


class FilterText(Filter):
    def fn_in(self, word: Token) -> bool:
        if self.list_have is None:
            return False
        return word.text in self.list_have

    def fn_not_in(self, word: Token) -> bool:
        if self.list_not_have is None:
            return False
        return word.text not in self.list_not_have
