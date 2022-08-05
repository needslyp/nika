"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Anastasiya Vasilevskaya
"""

import pymorphy2

from common import ScAddr, ScAgent, ScEventParams, ScModule, ScResult, ScType, ScTemplate
from common.sc_log import Log
from common_module.constant.identifiers import CommonIdentifiers, LangIdentifiers, MessageIdentifiers
from common_module.exception.custom_exception import CustomException
from common_module.searcher.common_constructions_searcher import get_action_argument, get_message_link
from common_module.generator.common_constructions_generator import generate_binary_relation
from message_classification_module.classifier.classifier import Classifier

from message_classification_module.constants.identifiers import ClassificationIdentifiers, WitIntentMessageClasses
from message_classification_module.constants.constants import (
    ResponseConstants,
    Idtf,
    IDTFS_FOR_SEARCH,
)
from message_classification_module.generator.generator import generate_message_specification

from requests.exceptions import ConnectionError  # pylint: disable=redefined-builtin


class MessageTopicClassificationAgent(ScAgent):
    def __init__(self, module: ScModule):
        super().__init__(module)
        self.action_node = None
        self.ctx = module.ctx
        self.log = Log(self.__class__.__name__)
        self.classifier = Classifier()
        self.morph_analyzer = pymorphy2.MorphAnalyzer()

    def RunImpl(self, evt: ScEventParams) -> ScResult:
        self.action_node = evt.other_addr
        status = ScResult.Ok

        if self.ctx.HelperCheckEdge(
            self.keynodes[ClassificationIdentifiers.ACTION_MESSAGE_TOPIC_CLASSIFICATION.value],
            self.action_node,
            ScType.EdgeAccessConstPosPerm,
        ):
            self.log.debug("MessageTopicClassificationAgent starts")
            try:
                message = get_action_argument(
                    self.ctx,
                    self.action_node,
                    CommonIdentifiers.RREL_ONE.value,
                    MessageIdentifiers.CONCEPT_MESSAGE.value,
                )
                message_classes, entities = self.classify_message(message)
                contour = self.ctx.CreateNode(ScType.NodeConstStruct)
                self.ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, message)
                rrel_entity = self.keynodes[Idtf.RREL_ENTITY.value]
                generate_message_specification(self.ctx, message, message_classes, entities, rrel_entity, contour)
                if contour is not None:
                    generate_binary_relation(
                        self.ctx,
                        self.action_node,
                        ScType.EdgeDCommonConst,
                        contour,
                        self.keynodes[CommonIdentifiers.NREL_ANSWER.value],
                    )
                self.ctx.CreateEdge(
                    ScType.EdgeAccessConstPosPerm,
                    self.keynodes[CommonIdentifiers.QUESTION_FINISHED_SUCCESSFULLY.value],
                    self.action_node,
                )
            except CustomException as ex:
                self.set_unsuccessful_status(str(ex))
                status = ScResult.Error
            except ConnectionError as ex:
                self.set_unsuccessful_status(str(ex))
                status = ScResult.Error
            finally:
                self.ctx.CreateEdge(
                    ScType.EdgeAccessConstPosPerm,
                    self.keynodes[CommonIdentifiers.QUESTION_FINISHED.value],
                    self.action_node,
                )
                self.log.debug("MessageTopicClassificationAgent has finished its work")

        return status

    def set_unsuccessful_status(self, error_message: str):
        self.log.error(error_message)
        self.ctx.CreateEdge(
            ScType.EdgeAccessConstPosPerm,
            self.keynodes[CommonIdentifiers.QUESTION_FINISHED_UNSUCCESSFULLY.value],
            self.action_node,
        )

    def classify_message(self, message: ScAddr):
        text_link = get_message_link(
            self.ctx, message, [CommonIdentifiers.CONCEPT_TEXT_FILE.value, LangIdentifiers.LANG_RU.value]
        )

        if text_link is None:
            raise CustomException(
                "MessageTopicClassificationAgent:"
                + "the message text link doesn't exist or it is in an unsupported language"
            )

        message_text = self.module.ctx.GetLinkContent(text_link)
        if message_text is None:
            raise CustomException("MessageTopicClassificationAgent: the message text link is empty")
        message_response = self.classifier.classify_message_topic(message_text.AsString())
        message_classes = [self.get_message_class_by_intent(message_response)]
        message_classes.extend(self.get_message_class_by_traits(message_response))
        entities = self.get_message_entities(message_response)
        return message_classes, entities

    def get_message_class_by_intent(self, wit_response):
        response_intent = None
        try:
            response_intent = wit_response[ResponseConstants.INTENTS.value]
        except TypeError as exception:
            self.log.error(str(exception))
        finally:
            if response_intent:
                intents_classes = self.get_wit_classes(Idtf.CONCEPT_INTENT_POSSIBLE_CLASS.value)
                templ_res = dict()
                for intent_class in intents_classes:
                    intent_idtfs = self.find_wit_id_by_node(intent_class)
                    for intent_idtf in intent_idtfs:
                        link_content = self.module.ctx.GetLinkContent(intent_idtf)
                        if link_content:
                            templ_res[link_content.AsString()] = intent_class
                wit_res = response_intent[0][ResponseConstants.NAME.value]
                class_node = templ_res.get(wit_res)
                if class_node is None:
                    class_node = self.keynodes[WitIntentMessageClasses.UNKNOWN_CLASS.value]
            else:
                class_node = self.keynodes[WitIntentMessageClasses.UNKNOWN_CLASS.value]
                self.log.warning("Message class by intent is unknown")
            if not class_node.IsValid:
                raise CustomException("Message class node is not found")
            self.log.debug("Found message class by intent: " + self.ctx.HelperGetSystemIdtf(class_node))
        return class_node

    def get_message_class_by_traits(  # noqa pylint: disable=too-many-branches disable=too-many-statements
        self, wit_response
    ) -> list:
        classes = []
        response_trait = None
        try:
            response_trait = wit_response[ResponseConstants.TRAITS.value]
        except TypeError as exception:
            self.log.error(str(exception))
        finally:
            if response_trait:
                class_names = self.get_wit_classes(Idtf.CONCEPT_TRAIT_POSSIBLE_CLASS.value)
                templ_res = dict()
                trait_idtf = None
                for class_name in class_names:
                    trait_template = ScTemplate()
                    trait_template.TripleWithRelation(
                        ScType.NodeVar >> "_trait_class",
                        ScType.EdgeDCommonVar,
                        class_name,
                        ScType.EdgeAccessVarPosPerm,
                        self.keynodes[CommonIdentifiers.NREL_INCLUSION.value],
                    )
                    result = self.ctx.HelperSearchTemplate(trait_template)
                    if result.Size() > 0:
                        wit_class_idtfs = self.find_wit_id_by_node(class_name)
                        for wit_class_idtf in wit_class_idtfs:
                            if wit_class_idtf:
                                for _ in range(result.Size()):
                                    link_content = self.module.ctx.GetLinkContent(wit_class_idtf)
                                    if link_content:
                                        templ_res[link_content.AsString()] = class_name
                                        trait_idtf = list(response_trait.keys())[0]
                class_node = None
                if trait_idtf and response_trait.get(trait_idtf):
                    self.log.debug("Found message class by trait: " + trait_idtf)
                    wit_res = response_trait.get(trait_idtf)[0][ResponseConstants.VALUE.value]
                    class_node = templ_res.get(wit_res)

                if class_node is None:
                    self.log.debug("Message class by trait node is not found")
                else:
                    classes.append(class_node)
        return classes

    def get_message_entities(self, wit_response) -> list:
        entities = []
        wit_entities = None
        try:
            response_entities = wit_response[ResponseConstants.ENTITIES.value].values()
            wit_entities = list(response_entities)
        except TypeError as exception:
            self.log.error(str(exception))
        finally:
            if wit_entities:
                for wit_entity in wit_entities:
                    for entity in wit_entity:
                        entity_node = self.find_entity(entity.get(ResponseConstants.VALUE.value))
                        if entity_node and entity_node not in entities:
                            self.log.debug("Found message entity node: " + self.ctx.HelperGetSystemIdtf(entity_node))
                            entities.append(entity_node)
            if not entities:
                self.log.warning("Message entity nodes are not found")
        return entities

    def get_wit_classes(self, wit_idtf: str) -> list:
        wit_classes = []
        template = ScTemplate()
        template.Triple(
            self.keynodes[wit_idtf],
            ScType.EdgeAccessVarPosPerm,
            ScType.NodeVar >> "_wit_class",
        )
        result = self.ctx.HelperSearchTemplate(template)
        if result.Size() > 0:
            for i in range(result.Size()):
                wit_classes.append(result[i]["_wit_class"])
        return wit_classes

    def get_class_idtf(self, entity_class: ScAddr, nrel_wit_ai: str) -> list:
        class_names = []
        template = ScTemplate()
        template.TripleWithRelation(
            entity_class,
            ScType.EdgeDCommonVar,
            ScType.NodeVar >> "_rrel",
            ScType.EdgeAccessVarPosPerm,
            self.keynodes[nrel_wit_ai],
        )
        template.Triple(
            "_rrel",
            ScType.EdgeAccessVarPosPerm,
            ScType.NodeVar >> "_class_name",
        )
        result = self.ctx.HelperSearchTemplate(template)
        if result.Size() > 0:
            for i in range(result.Size()):
                class_names.append(result[i]["_class_name"])
        return class_names

    def find_wit_id_by_node(self, wit_class, get_first=False):
        idtfs = []
        template = ScTemplate()
        template.TripleWithRelation(
            wit_class,
            ScType.EdgeDCommonVar,
            ScType.LinkVar >> "_idtf",
            ScType.EdgeAccessVarPosPerm,
            self.keynodes[Idtf.NREL_WIT_AI_IDTF.value],
        )
        result = self.ctx.HelperSearchTemplate(template)
        if result.Size() > 0:
            for i in range(result.Size()):
                idtfs.append(result[i]["_idtf"])
        if get_first:
            if idtfs:
                return idtfs[0]
        return idtfs

    # TODO: If "I" - return author of the message
    def find_entity(self, entity_text: str):  # noqa pylint: disable=too-many-branches
        entity_node = self.get_entity_node(entity_text)
        if entity_node:
            return entity_node
        entity_text_tokens = entity_text.split()
        if len(entity_text_tokens) > 1:
            capitalized_text = self.morph_analyzer.parse(entity_text_tokens[0])[0].normal_form
            capitalized_text = capitalized_text.capitalize()
            for token in entity_text_tokens[1:]:
                word = self.morph_analyzer.parse(token)[0].normal_form
                if token[0].isupper():
                    word = word.capitalize()
                capitalized_text += " " + word
        else:
            capitalized_text = self.morph_analyzer.parse(entity_text)[0].normal_form
            capitalized_text = capitalized_text.capitalize()

        entity_node = self.get_entity_node(capitalized_text)
        if entity_node:
            return entity_node

        text = ""
        entity_text_tokens = entity_text.split()
        if len(entity_text_tokens) > 1:
            for token in entity_text_tokens:
                token = self.morph_analyzer.parse(token)[0].normal_form
                if text:
                    text += " " + token
                else:
                    text += token
        else:
            text = self.morph_analyzer.parse(entity_text)[0].normal_form
        return self.get_entity_node(text)

    def get_entity_node(self, identifier: str) -> ScAddr:
        entity_node = None
        link_list = self.ctx.FindLinksByContent(identifier)
        for link in link_list:
            entity_node_alias = "_entity_node"

            for idtf in IDTFS_FOR_SEARCH:
                template = ScTemplate()
                template.TripleWithRelation(
                    ScType.NodeVar >> entity_node_alias,
                    ScType.EdgeDCommonVar,
                    link,
                    ScType.EdgeAccessVarPosPerm,
                    self.keynodes[idtf],
                )
                search_result = self.ctx.HelperSearchTemplate(template)
                if search_result.Size() > 0:
                    entity_node = search_result[0][entity_node_alias]
                    return entity_node

        return entity_node
