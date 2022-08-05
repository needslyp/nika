"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from enum import Enum


class CommonIdentifiers(Enum):
    ACTION_DEACTIVATED = "action_deactivated"

    CONCEPT_DIALOGUE = "concept_dialogue"
    CONCEPT_SOUND_FILE = "concept_sound_file"
    CONCEPT_TEXT_FILE = "concept_text_file"

    NREL_ANSWER = "nrel_answer"
    NREL_AUTHORS = "nrel_authors"
    NREL_INCLUSION = "nrel_inclusion"
    NREL_SC_TEXT_TRANSLATION = "nrel_sc_text_translation"
    NREL_VOICE_LANGUAGE = "nrel_voice_language"
    NREL_SUBDIVIDING = "nrel_subdividing"
    NREL_MAIN_IDTF = "nrel_main_idtf"
    NREL_IDTF = "nrel_idtf"

    RELATION = "relation"
    RREL_DYNAMIC_ARGUMENT = "rrel_dynamic_argument"
    RREL_ONE = "rrel_1"
    RREL_TWO = "rrel_2"
    RREL_NOT_MAXIMUM_STUDIED_OBJECT_CLASS = "rrel_not_maximum_studied_object_class"
    RREL_MAXIMUM_STUDIED_OBJECT_CLASS = "rrel_maximum_studied_object_class"
    RREL_EXPLORED_RELATION = "rrel_explored_relation"

    QUESTION = "question"
    QUESTION_FINISHED = "question_finished"
    QUESTION_FINISHED_SUCCESSFULLY = "question_finished_successfully"
    QUESTION_FINISHED_UNSUCCESSFULLY = "question_finished_unsuccessfully"
    QUESTION_INITIATED = "question_initiated"

    MYSELF = "Myself"


class MessageIdentifiers(Enum):
    CONCEPT_MESSAGE = "concept_message"
    CONCEPT_ATOMIC_MESSAGE = "concept_atomic_message"
    CONCEPT_NON_ATOMIC_MESSAGE = "concept_non_atomic_message"

    NREL_MESSAGE_SEQUENCE = "nrel_message_sequence"
    NREL_REPLY_MESSAGE = "nrel_reply"
    NREL_MESSAGE_DECOMPOSITION = "nrel_message_decomposition"


class TokenIdentifiers(Enum):
    CONCEPT_ENGLISH_TOKEN = "concept_english_token"
    CONCEPT_RUSSIAN_TOKEN = "concept_russian_token"
    CONCEPT_GERMAN_TOKEN = "concept_german_token"

    NREL_TOKEN_SEQUENCE = "nrel_token_sequence"
    NREL_DECOMPOSITION_INTO_TOKENS = "nrel_decomposition_into_tokens"
    NREL_TOKEN_LANGUAGE = "nrel_token_language"

    RREL_INITIAL_FORM = "rrel_initial_form"

    NREL_TOKEN = "nrel_token"


class LangIdentifiers(Enum):
    LANG_EN = "lang_en"
    LANG_DE = "lang_de"
    LANG_RU = "lang_ru"
    LANG_NONE = ""
    LANGUAGES = "languages"


class FormatIdentifiers(Enum):
    FORMAT = "format"
    FORMAT_AUDIO = "format_audio"
    FORMAT_M4A = "format_m4a"
    FORMAT_MP3 = "format_mp3"
    FORMAT_WAV = "format_wav"


IdentifiersEnums = [CommonIdentifiers, MessageIdentifiers, TokenIdentifiers, FormatIdentifiers, LangIdentifiers]
