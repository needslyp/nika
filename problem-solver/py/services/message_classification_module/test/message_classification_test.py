"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Nikiforov Sergei
Author Kseniya Bantsevich
Author Anastasiya Vasilevskaya
"""

from common_module.constant.identifiers import CommonIdentifiers, LangIdentifiers, MessageIdentifiers
from common_module.generator.common_constructions_generator import generate_link
from common_module.test_module.entity.agent_test_case import AgentTestCase
from common_module.test_module.generator.constructions_generator import generate_result
from common_module.test_module.generator.constructions_generator import generate_formed_message
from common_module.keynode.global_sc_keynodes import GlobalScKeynodes

from message_classification_module.constants.identifiers import ClassificationIdentifiers

from sc import ScMemoryContext, ScTemplate, ScType, ScAddr, ScTemplateParams


THIRD_PARTY_REPLY_WAIT_TIME = 30


class MessageTopicClassificationAgentTestCase(AgentTestCase):
    @classmethod
    def get_action_node(cls):
        return ClassificationIdentifiers.ACTION_MESSAGE_TOPIC_CLASSIFICATION.value

    def test_wrong_language_message(self):
        message = generate_formed_message(
            self.ctx,
            link_classes=[CommonIdentifiers.CONCEPT_TEXT_FILE.value, LangIdentifiers.LANG_EN.value],
            message_classes=[MessageIdentifiers.CONCEPT_ATOMIC_MESSAGE.value],
        )
        arguments = {message: False}
        self.assertTrue(
            emit_agent(
                self.ctx, arguments, [self.get_action_node()], CommonIdentifiers.QUESTION_FINISHED_UNSUCCESSFULLY
            )
        )

    def test_no_message(self):
        self.assertTrue(
            emit_agent(self.ctx, {}, [self.get_action_node()], CommonIdentifiers.QUESTION_FINISHED_UNSUCCESSFULLY)
        )

    def test_no_text(self):
        message = generate_formed_message(
            self.ctx,
            link_classes=[CommonIdentifiers.CONCEPT_TEXT_FILE.value, LangIdentifiers.LANG_RU.value],
            message_classes=[MessageIdentifiers.CONCEPT_ATOMIC_MESSAGE.value],
        )
        arguments = {message: False}
        self.assertTrue(
            emit_agent(
                self.ctx, arguments, [self.get_action_node()], CommonIdentifiers.QUESTION_FINISHED_UNSUCCESSFULLY
            )
        )


def generate_node_with_main_idtf(ctx: ScMemoryContext, main_idtf: str) -> ScAddr:
    keynodes = GlobalScKeynodes(ctx)

    idtf_link = generate_link(ctx, main_idtf)

    generated_node_alias = "_generated_node"
    template = ScTemplate()
    template.TripleWithRelation(
        ScType.NodeVar >> generated_node_alias,
        ScType.EdgeDCommonVar,
        idtf_link,
        ScType.EdgeAccessVarPosPerm,
        keynodes[CommonIdentifiers.NREL_MAIN_IDTF.value],
    )
    template_generation_params = ScTemplateParams()
    gen_result = ctx.HelperGenTemplate(template, template_generation_params)

    return gen_result[generated_node_alias]


def emit_agent(
    ctx: ScMemoryContext, arguments: dict, concepts: list, reaction=CommonIdentifiers.QUESTION_FINISHED_UNSUCCESSFULLY
) -> bool:

    return generate_result(
        ctx,
        arguments,
        concepts,
        initiation=CommonIdentifiers.QUESTION_INITIATED,
        reaction=reaction,
        wait_time=THIRD_PARTY_REPLY_WAIT_TIME,
    )
