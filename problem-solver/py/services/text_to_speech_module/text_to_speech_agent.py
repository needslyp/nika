"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

import base64

from common import ScAgent, ScEventParams
from common.sc_log import Log
from common_module.constant.identifiers import CommonIdentifiers, FormatIdentifiers, LangIdentifiers, MessageIdentifiers
from common_module.exception.custom_exception import CustomException
from common_module.generator.common_constructions_generator import generate_binary_relation, generate_link
from common_module.searcher.common_constructions_searcher import (
    get_action_argument,
    get_link_language_class,
    get_message_link,
)
from sc import ScAddr, ScResult, ScType
from text_to_speech_module.constant.synthesizer_identifiers import SynthesizerIdentifiers
from text_to_speech_module.synthesizer.base_synthesizer import BaseSynthesizer


class TextToSpeechAgent(ScAgent):
    def __init__(self, module, synthesizer: BaseSynthesizer):
        super().__init__(module)
        self.keynodes = module.keynodes
        self.ctx = module.ctx
        self.main_node = None
        self.synthesizer = synthesizer
        self.log = Log(self.__class__.__name__)

    def RunImpl(self, evt: ScEventParams) -> ScResult:
        self.main_node = evt.other_addr
        status = ScResult.Ok

        if self.module.ctx.HelperCheckEdge(
            self.keynodes[SynthesizerIdentifiers.ACTION_SYNTHESIZE_SPEECH.value],
            self.main_node,
            ScType.EdgeAccessConstPosPerm,
        ):
            self.log.debug("TextToSpeechAgent starts")
            try:
                if self.main_node is None or not self.main_node.IsValid():  # if not self.main_node.IsValid():
                    raise CustomException("The question node isn't valid.")

                message = get_action_argument(
                    self.ctx, self.main_node, CommonIdentifiers.RREL_ONE.value, MessageIdentifiers.CONCEPT_MESSAGE.value
                )
                message_link = self.get_message_link(message)
                message_text = self.ctx.GetLinkContent(message_link).AsString()
                lang = get_link_language_class(self.ctx, message_link)
                audio_content = self.synthesizer.synthesize_voice(text=message_text, lang=lang)

                contour = self.ctx.CreateNode(ScType.NodeConstStruct)
                self.generate_sound(audio_content, lang, message, contour)

                self.ctx.CreateEdge(
                    ScType.EdgeAccessConstPosPerm,
                    self.keynodes[CommonIdentifiers.QUESTION_FINISHED_SUCCESSFULLY.value],
                    self.main_node,
                )
            except CustomException as ex:
                self.set_unsuccessful_status(str(ex))
                status = ScResult.Error
            finally:
                self.ctx.CreateEdge(
                    ScType.EdgeAccessConstPosPerm,
                    self.keynodes[CommonIdentifiers.QUESTION_FINISHED.value],
                    self.main_node,
                )

            self.log.debug("TextToSpeechAgent has finished its work")
        return status

    def get_message_link(self, message: ScAddr) -> ScAddr:
        link = get_message_link(self.module.ctx, message, [CommonIdentifiers.CONCEPT_TEXT_FILE.value])

        if link is None:
            raise CustomException("The message doesn't has sc-link with message text.")

        return link

    def generate_sound(self, audio_content, lang: str, message: ScAddr, contour=None):
        link = self.generate_sound_link(audio_content, lang, contour)
        text_translation_node = self.ctx.CreateNode(ScType.NodeConst)
        nrel_sc_text_translation = self.keynodes[CommonIdentifiers.NREL_SC_TEXT_TRANSLATION.value]
        d_common_edge = self.ctx.CreateEdge(ScType.EdgeDCommonConst, text_translation_node, message)
        access_edge = self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, nrel_sc_text_translation, d_common_edge)
        text_translation_edge = self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, text_translation_node, link)
        elements = [
            text_translation_node,
            nrel_sc_text_translation,
            d_common_edge,
            access_edge,
            text_translation_edge,
            message,
        ]

        if contour is not None:
            generate_binary_relation(
                self.ctx,
                self.main_node,
                ScType.EdgeDCommonConst,
                contour,
                self.keynodes[CommonIdentifiers.NREL_ANSWER.value],
            )
            for element in elements:
                self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, element)

    def generate_sound_link(self, audio_content, lang_class: str, contour=None):
        link = generate_link(self.ctx, base64.b64encode(audio_content))
        format_wav = self.keynodes[FormatIdentifiers.FORMAT_WAV.value]
        format_wav_edge = self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, format_wav, link)
        concept_sound_file = self.keynodes[CommonIdentifiers.CONCEPT_SOUND_FILE.value]
        sound_file_edge = self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, concept_sound_file, link)
        elements = [link, format_wav, format_wav_edge, concept_sound_file, sound_file_edge]

        if lang_class != LangIdentifiers.LANG_NONE.value:
            lang_class_node = self.keynodes[lang_class]
            lang_edge = self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, lang_class_node, link)
            elements.append(lang_class_node)
            elements.append(lang_edge)

        if contour is not None:
            for element in elements:
                self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, element)

        return link

    def set_unsuccessful_status(self, error_message: str):
        self.log.error(error_message)
        self.ctx.CreateEdge(
            ScType.EdgeAccessConstPosPerm,
            self.keynodes[CommonIdentifiers.QUESTION_FINISHED_UNSUCCESSFULLY.value],
            self.main_node,
        )
