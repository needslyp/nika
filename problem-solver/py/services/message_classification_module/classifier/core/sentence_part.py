"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""


from typing import List

from spacy.tokens import Token

from message_classification_module.classifier.core.constants import spacy_dep_constants as sdc


class SentencePart:
    def __init__(self):
        self.dep_list = [sdc.PD, sdc.OPRD, sdc.SP]

    def __call__(self, sentences: List[List[Token]]) -> List[List[Token]]:
        return self.sentences_part(sentences)

    def sentence_part(self, sentence: List[Token]) -> List[List[Token]]:
        result = list()
        new_sentence = list()
        for word in sentence:
            if word not in self.dep_list:
                new_sentence.append(word)
            else:
                result.append(new_sentence)
                new_sentence.clear()
        if len(new_sentence) > 0:
            result.append(new_sentence)
        return result

    def sentences_part(self, sentences: List[List[Token]]) -> List[List[Token]]:
        result = list()
        for sentence in sentences:
            sentence_part = self.sentence_part(sentence)
            if sentence_part is not None:
                result += sentence_part
        return result
