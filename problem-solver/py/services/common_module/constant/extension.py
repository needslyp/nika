"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from enum import Enum

from common_module.constant.identifiers import FormatIdentifiers


class AudioExtension(Enum):
    MP3 = "mp3"
    M4A = "m4a"
    WAV = "wav"
    NOT_SETTED = ""


class PyTorchExtension(Enum):
    PT = "pt"


class StatExtension(Enum):
    STAT = "stat"


AUDIO_FORMATS = {
    FormatIdentifiers.FORMAT_MP3.value: AudioExtension.MP3.value,
    FormatIdentifiers.FORMAT_M4A.value: AudioExtension.M4A.value,
    FormatIdentifiers.FORMAT_WAV.value: AudioExtension.WAV.value,
}
