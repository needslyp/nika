"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""
from speech_to_text_module.recognizer.recognizer import AzureRecognizer, BaseRecognizer
from speech_to_text_module.recognizer.vosk_recognizer import VoskRecognizer


class BaseRecognizerFactory:
    def generate_recognizer(self) -> BaseRecognizer:
        raise NotImplementedError('Method "generate_recognizer" isn\'t implemented.')


class AzureRecognizerFactory(BaseRecognizerFactory):
    def generate_recognizer(self) -> AzureRecognizer:
        return AzureRecognizer()


class VoskRecognizerFactory(BaseRecognizerFactory):
    def generate_recognizer(self) -> VoskRecognizer:
        return VoskRecognizer()
