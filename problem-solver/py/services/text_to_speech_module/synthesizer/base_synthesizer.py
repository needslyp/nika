"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from abc import ABC, abstractmethod

from text_to_speech_module.entity.voice import Voice


class BaseSynthesizer(ABC):
    def __init__(self, voices: dict):
        self.voices = voices

    @abstractmethod
    def synthesize_voice(self, text: str, lang: str):
        raise NotImplementedError('Method "synthesize_voice" isn\'t implemented.')

    def set_voices(self, voices: dict):
        self.voices = voices

    def _choose_voice(self, lang: str) -> Voice:
        voice = None
        if lang in self.voices:
            voice = self.voices[lang]
        return voice
