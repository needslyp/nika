"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from common import ScAgent, ScEventParams
from common.sc_log import Log
from common_module.constant.identifiers import CommonIdentifiers, LangIdentifiers, MessageIdentifiers
from common_module.constant.messages import MessageTexts
from common_module.exception.custom_exception import CustomException
from common_module.generator.common_constructions_generator import generate_binary_relation, generate_link
from common_module.keynode.global_sc_keynodes import GlobalScKeynodes
from common_module.searcher.common_constructions_searcher import (
    get_action_argument,
    get_link_language_class,
    get_message_link,
)
from sc import ScAddr, ScResult, ScType
from speech_to_text_module.constant.recognizer_constants import RecognizerIdentifiers
from speech_to_text_module.recognizer.recognizer import BaseRecognizer


class SpeechToTextAgent(ScAgent):
    def __init__(self, module, recognizer: BaseRecognizer):
        super().__init__(module)
        self.ctx = module.ctx
        self.keynodes = GlobalScKeynodes(self.ctx)
        self.main_node = None
        self.recognizer = recognizer
        self.log = Log(self.__class__.__name__)

    def RunImpl(self, evt: ScEventParams) -> ScResult:
        self.main_node = evt.other_addr
        status = ScResult.Ok

        if self.module.ctx.HelperCheckEdge(
            self.keynodes[RecognizerIdentifiers.ACTION_RECOGNIZE_TEXT.value],
            self.main_node,
            ScType.EdgeAccessConstPosPerm,
        ):
            self.log.debug("SpeechToTextAgent starts")

            try:
                if self.main_node is None or not self.main_node.IsValid():
                    raise CustomException("The question node isn't valid.")

                message = get_action_argument(
                    self.ctx, self.main_node, CommonIdentifiers.RREL_ONE.value, MessageIdentifiers.CONCEPT_MESSAGE.value
                )
                text_link = get_message_link(self.ctx, message, [CommonIdentifiers.CONCEPT_TEXT_FILE.value])
                if text_link is None:
                    speech_link = self.get_speech_link(message)
                    lang = get_link_language_class(self.ctx, speech_link)
                    text_result = self.recognize_text(speech_link, lang)
                    contour = self.ctx.CreateNode(ScType.NodeConstStruct)
                    self.generate_text_message(text_result, lang, message, contour)
                else:
                    self.log.debug("SpeechToTextAgent: the message text already exists")
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

            self.log.debug("SpeechToTextAgent has finished its work")
        return status

    def get_speech_link(self, message: ScAddr) -> ScAddr:
        concepts = [CommonIdentifiers.CONCEPT_SOUND_FILE.value]
        link = get_message_link(self.module.ctx, message, concepts)

        if link is None:
            raise CustomException("The message doesn't has sc-link with speech.")

        return link

    def recognize_text(self, speech_link: ScAddr, lang: str):
        self.log.debug("Text's language: {}".format(lang))
        speech_string = self.ctx.GetLinkContent(speech_link).AsString()
        try:
            text_result = self.recognizer.recognize_text(speech_string, lang)
            if text_result == "":
                self.log.debug("Recognized text is empty.")
                text_result = MessageTexts.EMPTY_MESSAGE_TEXT.value
        except CustomException as ex:
            self.log.debug(str(ex))
            text_result = MessageTexts.EMPTY_MESSAGE_TEXT.value
        self.log.debug("Recognized text set as: {}".format(text_result))
        return text_result

    def generate_text_message(self, text_message: str, lang: str, message: ScAddr, contour=None):
        link = self.generate_text_link(text_message, lang, contour)
        text_translation_node = self.ctx.CreateNode(ScType.NodeConst)
        nrel_sc_text_translation = self.keynodes[CommonIdentifiers.NREL_SC_TEXT_TRANSLATION.value]
        d_common_edge = self.ctx.CreateEdge(ScType.EdgeDCommonConst, text_translation_node, message)
        access_edge = self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, nrel_sc_text_translation, d_common_edge)
        text_translation_edge = self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, text_translation_node, link)
        elements = [
            message,
            text_translation_node,
            nrel_sc_text_translation,
            d_common_edge,
            access_edge,
            text_translation_edge,
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

    def generate_text_link(self, text_message: str, lang_class: str, contour=None):
        link = generate_link(self.ctx, text_message)

        if lang_class != LangIdentifiers.LANG_NONE.value:
            lang_class_node = self.keynodes[lang_class]
            lang_edge = self.module.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, lang_class_node, link)
            if contour is not None:
                self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, lang_class_node)
                self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, lang_edge)

        concept_text_file = self.keynodes[CommonIdentifiers.CONCEPT_TEXT_FILE.value]
        file_type_edge = self.module.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, concept_text_file, link)

        if contour is not None:
            self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, concept_text_file)
            self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, file_type_edge)
            self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, link)

        return link

    def set_unsuccessful_status(self, error_message: str):
        self.log.error(error_message)
        self.module.ctx.CreateEdge(
            ScType.EdgeAccessConstPosPerm,
            self.keynodes[CommonIdentifiers.QUESTION_FINISHED_UNSUCCESSFULLY.value],
            self.main_node,
        )
