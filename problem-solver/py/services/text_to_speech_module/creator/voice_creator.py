"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from common_module.exception.custom_exception import CustomException
from sc import ScAddr, ScMemoryContext
from text_to_speech_module.constant.synthesizer_identifiers import SynthesizerIdentifiers
from text_to_speech_module.entity.voice import Voice
from text_to_speech_module.searcher.voice_searcher import (
    check_affiliation,
    get_sex,
    get_synthesizer,
    get_voice_id,
    get_voice_language,
)


def create_voice(ctx: ScMemoryContext, voice_node: ScAddr) -> Voice:
    if not voice_node.IsValid():
        raise CustomException("The synthesizer ScAddr isn't valid.")

    voice = Voice()

    voice.id = get_voice_id(ctx, voice_node)
    voice.synthesizer = get_synthesizer(ctx, voice_node)
    voice.sex = get_sex(ctx, voice_node)
    voice.lang = get_voice_language(ctx, voice_node)
    voice.is_standard = check_affiliation(ctx, voice_node, SynthesizerIdentifiers.CONCEPT_STANDARD_SYNTHESIZER_VOICE)
    voice.is_neural = check_affiliation(ctx, voice_node, SynthesizerIdentifiers.CONCEPT_NEURAL_SYNTHESIZER_VOICE)

    return voice
