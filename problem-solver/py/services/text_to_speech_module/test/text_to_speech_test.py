"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from common_module.constant.identifiers import CommonIdentifiers, LangIdentifiers
from common_module.generator.common_constructions_generator import generate_link, generate_message
from common_module.test_module.entity.agent_test_case import AgentTestCase
from common_module.test_module.generator.constructions_generator import generate_result
from sc import ScMemoryContext, ScType
from text_to_speech_module.constant.synthesizer_identifiers import SynthesizerIdentifiers

TEXT_TO_SPEECH_WAIT_TIME = 5


class TextToSpeechAgentTestCase(AgentTestCase):
    ENGLISH_MESSAGE = "Hello. It's me."
    RUSSIAN_MESSAGE = "Привет. Это я."

    @classmethod
    def get_action_node(cls):
        return SynthesizerIdentifiers.ACTION_SYNTHESIZE_SPEECH.value

    # pylint: disable=all
    def test_message_is_not_set(self):
        result = emit_agent(self.ctx, {}, [self.get_action_node()])
        self.assertTrue(result)

    def test_message_is_not_message(self):
        message = self.ctx.CreateNode(ScType.NodeConst)

        arguments = {message: False}
        result = emit_agent(self.ctx, arguments, [self.get_action_node()])
        self.assertTrue(result)

    def test_message_does_not_have_sc_link(self):
        message = generate_message(self.ctx, {})

        arguments = {message: False}
        result = emit_agent(self.ctx, arguments, [self.get_action_node()])
        self.assertTrue(result)

    def test_sc_link_does_not_have_lang(self):
        text_link = generate_link(self.ctx, self.ENGLISH_MESSAGE)
        message = generate_message(self.ctx, {text_link: []})

        arguments = {message: False}
        result = emit_agent(self.ctx, arguments, [self.get_action_node()])
        self.assertTrue(result)

    def test_english_message_is_correct(self):
        params = [self.ctx, self.ENGLISH_MESSAGE, LangIdentifiers.LANG_EN, False]
        result = message_is_correct(*params)
        self.assertTrue(result)

    def test_russian_message_is_correct(self):
        params = [self.ctx, self.RUSSIAN_MESSAGE, LangIdentifiers.LANG_RU, False]
        result = message_is_correct(*params)
        self.assertTrue(result)

    def test_english_message_is_correct_dynamic_argument(self):
        params = [self.ctx, self.ENGLISH_MESSAGE, LangIdentifiers.LANG_EN, True]
        result = message_is_correct(*params)
        self.assertTrue(result)

    def test_russian_message_is_correct_dynamic_argument(self):
        params = [self.ctx, self.RUSSIAN_MESSAGE, LangIdentifiers.LANG_RU, True]
        result = message_is_correct(*params)
        self.assertTrue(result)


def message_is_correct(ctx: ScMemoryContext, text: str, lang: LangIdentifiers, is_dynamic: bool) -> bool:
    text_link = generate_link(ctx, text)
    text_link_concepts = [lang.value, CommonIdentifiers.CONCEPT_TEXT_FILE.value]
    message = generate_message(ctx, {text_link: text_link_concepts})

    arguments = {message: is_dynamic}
    concepts = [SynthesizerIdentifiers.ACTION_SYNTHESIZE_SPEECH.value]
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
        wait_time=TEXT_TO_SPEECH_WAIT_TIME,
    )
    return result
