"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from enum import Enum


class SynthesizerIdentifiers(Enum):
    ACTION_SYNTHESIZE_SPEECH = "action_synthesize_speech"

    CONCEPT_SYNTHESIZER = "concept_synthesizer"
    CONCEPT_EN_SYNTHESIZER_VOICE = "concept_en_synthesizer_voice"
    CONCEPT_RU_SYNTHESIZER_VOICE = "concept_ru_synthesizer_voice"
    CONCEPT_FEMALE_SYNTHESIZER_VOICE = "concept_female_synthesizer_voice"
    CONCEPT_MALE_SYNTHESIZER_VOICE = "concept_male_synthesizer_voice"
    CONCEPT_STANDARD_SYNTHESIZER_VOICE = "concept_standard_synthesizer_voice"
    CONCEPT_NEURAL_SYNTHESIZER_VOICE = "concept_neural_synthesizer_voice"
    CONCEPT_AZURE_SYNTHESIZER_VOICE = "concept_azure_synthesizer_voice"
    CONCEPT_AWS_POLLY_SYNTHESIZER_VOICE = "concept_aws_polly_synthesizer_voice"

    NREL_SYNTHESIZER = "nrel_synthesizer"
    NREL_CURRENT_VOICES = "nrel_current_voices"
    NREL_VOICE_ID = "nrel_voice_id"
    NREL_SUPPORTED_VOICES = "nrel_supported_voices"

    SYNTHESIZER_AWS_POLLY = "synthesizer_aws_polly"
    SYNTHESIZER_AZURE = "synthesizer_azure"


VOICES_CLASSES_BY_SEX = {
    SynthesizerIdentifiers.CONCEPT_FEMALE_SYNTHESIZER_VOICE.value,
    SynthesizerIdentifiers.CONCEPT_MALE_SYNTHESIZER_VOICE.value,
}

VOICES_CLASSES_BY_LANGUAGE = {
    SynthesizerIdentifiers.CONCEPT_EN_SYNTHESIZER_VOICE.value,
    SynthesizerIdentifiers.CONCEPT_RU_SYNTHESIZER_VOICE.value,
}
