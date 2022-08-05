"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

import base64
import os
import unittest

from common import ScMemoryContext
from common_module.constant.identifiers import CommonIdentifiers, FormatIdentifiers, LangIdentifiers
from common_module.generator.common_constructions_generator import generate_link, generate_message
from common_module.test_module.entity.agent_test_case import AgentTestCase
from common_module.test_module.generator.constructions_generator import generate_result
from common_module.searcher.common_constructions_searcher import get_message_link_list
from sc import ScAddr, ScType
from speech_to_text_module.constant.recognizer_constants import AzureLangNames, RecognizerIdentifiers

SPEECH_TO_TEXT_WAIT_TIME = 5


class SpeechToTextAgentTestCase(AgentTestCase):
    SPEECHES = {
        AzureLangNames.EN: "speeches/english_speech.wav",
        AzureLangNames.DE: "speeches/german_speech.wav",
        AzureLangNames.RU: "speeches/russian_speech.wav",
    }

    @classmethod
    def get_action_node(cls):
        return RecognizerIdentifiers.ACTION_RECOGNIZE_TEXT.value

    def test_message_is_not_set(self):
        result = emit_agent(self.ctx, {}, [self.get_action_node()])
        self.assertTrue(result)

    def test_message_is_not_message(self):
        message = self.ctx.CreateNode(ScType.NodeConst)

        arguments = {message: False}
        result = emit_agent(self.ctx, arguments, [self.get_action_node()])
        self.assertTrue(result)

    def test_message_doesnt_has_sc_link(self):
        message = generate_message(self.ctx, {})

        arguments = {message: False}
        result = emit_agent(self.ctx, arguments, [self.get_action_node()])
        self.assertTrue(result)

    def test_message_link_isnt_sound_file(self):
        speech_link = generate_link(self.ctx, read_speech(self.SPEECHES[AzureLangNames.EN]))
        message = generate_message(self.ctx, {speech_link: []})

        arguments = {message: False}
        result = emit_agent(self.ctx, arguments, [self.get_action_node()])
        self.assertTrue(result)

    def test_message_speech_doesnt_has_lang(self):
        speech_link = generate_link(self.ctx, read_speech(self.SPEECHES[AzureLangNames.EN]))
        speech_link_concepts = [CommonIdentifiers.CONCEPT_SOUND_FILE.value]
        message = generate_message(self.ctx, {speech_link: speech_link_concepts})

        arguments = {message: False}
        result = emit_agent(self.ctx, arguments, [self.get_action_node()])
        self.assertTrue(result)

    def test_message_text_is_already_exists(self):
        speech_link = generate_link(self.ctx, read_speech(self.SPEECHES[AzureLangNames.EN]))
        speech_link_concepts = [
            CommonIdentifiers.CONCEPT_SOUND_FILE.value,
            FormatIdentifiers.FORMAT_WAV.value,
            LangIdentifiers.LANG_EN.value,
        ]
        text_link = generate_link(self.ctx, "some text")
        text_link_concepts = [CommonIdentifiers.CONCEPT_TEXT_FILE.value, LangIdentifiers.LANG_EN.value]
        message = generate_message(self.ctx, {speech_link: speech_link_concepts, text_link: text_link_concepts})

        arguments = {message: False}
        result = emit_agent(
            self.ctx, arguments, [self.get_action_node()], CommonIdentifiers.QUESTION_FINISHED_SUCCESSFULLY
        )
        self.assertTrue(result)
        self.assertTrue(is_message_have_only_one_link(self.ctx, message))

    def test_english_message_is_correct(self):
        params = [self.ctx, self.SPEECHES[AzureLangNames.EN], LangIdentifiers.LANG_EN, False]
        result = message_is_correct(*params)
        self.assertTrue(result)

    @unittest.skip
    def test_german_message_is_correct(self):
        params = [self.ctx, self.SPEECHES[AzureLangNames.DE], LangIdentifiers.LANG_DE, False]
        result = message_is_correct(*params)
        self.assertTrue(result)

    def test_russian_message_is_correct(self):
        params = [self.ctx, self.SPEECHES[AzureLangNames.RU], LangIdentifiers.LANG_RU, False]
        result = message_is_correct(*params)
        self.assertTrue(result)

    def test_english_message_is_correct_dynamic_argument(self):
        params = [self.ctx, self.SPEECHES[AzureLangNames.EN], LangIdentifiers.LANG_EN, True]
        result = message_is_correct(*params)
        self.assertTrue(result)

    @unittest.skip
    def test_german_message_is_correct_dynamic_argument(self):
        params = [self.ctx, self.SPEECHES[AzureLangNames.DE], LangIdentifiers.LANG_DE, True]
        result = message_is_correct(*params)
        self.assertTrue(result)

    def test_russian_message_is_correct_dynamic_argument(self):
        params = [self.ctx, self.SPEECHES[AzureLangNames.RU], LangIdentifiers.LANG_RU, True]
        result = message_is_correct(*params)
        self.assertTrue(result)


def message_is_correct(ctx: ScMemoryContext, speech_file: str, lang: LangIdentifiers, is_dynamic: bool) -> bool:
    speech_link = generate_link(ctx, read_speech(speech_file))
    speech_link_concepts = [CommonIdentifiers.CONCEPT_SOUND_FILE.value, FormatIdentifiers.FORMAT_WAV.value, lang.value]
    message = generate_message(ctx, {speech_link: speech_link_concepts})

    arguments = {message: is_dynamic}
    concepts = [RecognizerIdentifiers.ACTION_RECOGNIZE_TEXT.value]
    result = emit_agent(ctx, arguments, concepts, reaction=CommonIdentifiers.QUESTION_FINISHED_SUCCESSFULLY)
    return result


def emit_agent(
    ctx: ScMemoryContext, arguments: dict, concepts: list, reaction=CommonIdentifiers.QUESTION_FINISHED_UNSUCCESSFULLY
) -> bool:

    result = generate_result(
        ctx,
        arguments,
        concepts,
        initiation=CommonIdentifiers.QUESTION_INITIATED,
        reaction=reaction,
        wait_time=SPEECH_TO_TEXT_WAIT_TIME,
    )
    return result


def read_speech(file_path: str):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
    with open(file_path, "rb") as file:
        speech = base64.b64encode(file.read())
    return speech


def is_message_have_only_one_link(ctx: ScMemoryContext, message: ScAddr):
    message_links = get_message_link_list(ctx, message, [CommonIdentifiers.CONCEPT_TEXT_FILE.value])
    return len(message_links) == 1
