"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from common_module.exception.custom_exception import CustomException
from sc import ScAddr, ScMemoryContext
from text_to_speech_module.searcher.synthesizer_searcher import get_current_synthesizer_voices
from text_to_speech_module.synthesizer.base_synthesizer import BaseSynthesizer


class BaseSynthesizerFactory:
    def create_synthesizer(self, ctx: ScMemoryContext, synthesizer_node: ScAddr) -> BaseSynthesizer:
        pass

    def get_voices(self, ctx: ScMemoryContext, synthesizer_node: ScAddr):
        voices = get_current_synthesizer_voices(ctx, synthesizer_node)

        if not voices:
            raise CustomException("Synthesizer wasn't created because current voices weren't found.")

        return voices
