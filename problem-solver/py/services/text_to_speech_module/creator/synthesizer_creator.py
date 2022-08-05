"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from common_module.exception.custom_exception import CustomException
from sc import ScMemoryContext
from text_to_speech_module.constant.synthesizer_identifiers import SynthesizerIdentifiers
from text_to_speech_module.creator.synthesizer_factory.aws_polly_synthesizer_factory import AwsPollySynthesizerFactory
from text_to_speech_module.creator.synthesizer_factory.azure_synthesizer_factory import AzureSynthesizerFactory
from text_to_speech_module.searcher.synthesizer_searcher import get_system_synthesizer
from text_to_speech_module.synthesizer.base_synthesizer import BaseSynthesizer

SYNTHESIZER_FACTORIES = {
    SynthesizerIdentifiers.SYNTHESIZER_AZURE.value: AzureSynthesizerFactory(),
    SynthesizerIdentifiers.SYNTHESIZER_AWS_POLLY.value: AwsPollySynthesizerFactory(),
}


def create_synthesizer(ctx: ScMemoryContext) -> BaseSynthesizer:
    synthesizer_node = get_system_synthesizer(ctx)
    synthesizer_name = ctx.HelperGetSystemIdtf(synthesizer_node)

    if synthesizer_name not in SYNTHESIZER_FACTORIES.keys():
        raise CustomException('Agent doesn\'t support the synthesizer "{}".'.format(synthesizer_name))

    synthesizer = SYNTHESIZER_FACTORIES[synthesizer_name].create_synthesizer(ctx, synthesizer_node)

    return synthesizer
