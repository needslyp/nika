"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from common_module.constant.identifiers import LangIdentifiers
from text_to_speech_module.constant.synthesizer_constants import Sex, Synthesizers


class Voice:
    def __init__(self):
        self.id = ""
        self.synthesizer = Synthesizers.NOT_SETTED
        self.sex = Sex.NOT_SETTED
        self.lang = LangIdentifiers.LANG_NONE
        self.is_standard = False
        self.is_neural = False

    def __str__(self):
        return "voice: {}\nsynthesizer: {}\nsex: {}\nlang: {}\nis standard: {}\nis neural: {}".format(
            self.id, self.synthesizer.value, self.sex.value, self.lang.value, self.is_standard, self.is_neural
        )
