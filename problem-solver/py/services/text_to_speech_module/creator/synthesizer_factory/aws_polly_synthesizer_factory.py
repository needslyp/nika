"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from sc import ScAddr, ScMemoryContext
from text_to_speech_module.creator.synthesizer_factory.base_synthesizer_factory import BaseSynthesizerFactory
from text_to_speech_module.synthesizer.aws_polly_synthesizer import AwsPollySynthesizer


class AwsPollySynthesizerFactory(BaseSynthesizerFactory):
    def create_synthesizer(self, ctx: ScMemoryContext, synthesizer_node: ScAddr) -> AwsPollySynthesizer:
        voices = self.get_voices(ctx, synthesizer_node)
        return AwsPollySynthesizer(voices)
