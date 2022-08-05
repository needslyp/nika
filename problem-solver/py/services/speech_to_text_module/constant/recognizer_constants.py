"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from enum import Enum

from common_module.constant.identifiers import LangIdentifiers


class RecognizerIdentifiers(Enum):
    ACTION_RECOGNIZE_TEXT = "action_recognize_text"
    CONCEPT_RECOGNIZER = "concept_recognizer"
    NREL_RECOGNIZER = "nrel_recognizer"
    RECOGNIZER_AZURE = "recognizer_azure"
    RECOGNIZER_VOSK = "recognizer_vosk"


class AzureLangNames(Enum):
    EN = "en-US"
    DE = "de-DE"
    RU = "ru-RU"
    NOT_SETTED = ""


class VoskLangNames(Enum):
    EN = "en"
    DE = "de"
    RU = "ru"
    NOT_SETTED = ""


AZURE_SPEECH_TO_TEXT_LANGS = {key.value: value for (key, value) in zip(LangIdentifiers, AzureLangNames)}

VOSK_SPEECH_TO_TEXT_LANGS = {key.value: value for (key, value) in zip(LangIdentifiers, VoskLangNames)}
