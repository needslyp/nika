"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from common_module.exception.custom_exception import CustomException
from sc import ScMemoryContext
from speech_to_text_module.constant.recognizer_constants import RecognizerIdentifiers
from speech_to_text_module.creator.factory.recognizer_factory import AzureRecognizerFactory, VoskRecognizerFactory
from speech_to_text_module.searcher.recognizer_searcher import get_system_recognizer

RECOGNIZER_FACTORIES = {
    RecognizerIdentifiers.RECOGNIZER_AZURE.value: AzureRecognizerFactory(),
    RecognizerIdentifiers.RECOGNIZER_VOSK.value: VoskRecognizerFactory(),
}


def create_recognizer(ctx: ScMemoryContext):
    recognizer_node = get_system_recognizer(ctx)
    recognizer_name = ctx.HelperGetSystemIdtf(recognizer_node)
    if recognizer_name not in RECOGNIZER_FACTORIES.keys():
        raise CustomException('Agent doesn\'t support the recognizer "{}".'.format(recognizer_name))
    recognizer = RECOGNIZER_FACTORIES[recognizer_name].generate_recognizer()
    return recognizer
