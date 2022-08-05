"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from enum import Enum

from text_to_speech_module.constant.synthesizer_identifiers import SynthesizerIdentifiers


class Engine(Enum):
    STANDARD = "standard"
    NEURAL = "neural"


class Sex(Enum):
    FEMALE = "female"
    MALE = "male"
    NOT_SETTED = ""


class Synthesizers(Enum):
    AWS_POLLY = "aws polly"
    AZURE = "azure"
    NOT_SETTED = ""


SYNTHESIZERS = {
    SynthesizerIdentifiers.CONCEPT_AWS_POLLY_SYNTHESIZER_VOICE.value: Synthesizers.AWS_POLLY,
    SynthesizerIdentifiers.CONCEPT_AZURE_SYNTHESIZER_VOICE.value: Synthesizers.AZURE,
}

VOICES_SEX = {
    SynthesizerIdentifiers.CONCEPT_FEMALE_SYNTHESIZER_VOICE.value: Sex.FEMALE,
    SynthesizerIdentifiers.CONCEPT_MALE_SYNTHESIZER_VOICE.value: Sex.MALE,
}
