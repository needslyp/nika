"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from common_module.constant.identifiers import CommonIdentifiers, MessageIdentifiers
from common_module.constant.prefix import SystemIdentifierPrefixes
from common_module.generator.common_constructions_generator import (
    generate_binary_relation,
    generate_message,
    generate_link,
)
from common_module.generator.token_constructions_generator import generate_decomposition_into_tokens
from common_module.keynode.global_sc_keynodes import GlobalScKeynodes
from common_module.test_module.entity.agent_test import COMMON_WAIT_TIME, wait_agent
from sc import ScAddr, ScMemoryContext, ScTemplate, ScTemplateParams, ScType


def generate_action_with_arguments(ctx: ScMemoryContext, arguments: dict, concepts: list) -> ScAddr:
    action = generate_action(ctx, concepts)
    keynodes = GlobalScKeynodes(ctx)

    for index, argument in enumerate(arguments, 1):
        if argument.IsValid():
            rrel_identifier = "{}{}".format(SystemIdentifierPrefixes.RREL_.value, str(index))
            is_dynamic = arguments[argument]
            if is_dynamic:
                variable = ctx.CreateNode(ScType.NodeConst)
                generate_binary_relation(
                    ctx,
                    action,
                    ScType.EdgeAccessConstPosPerm,
                    variable,
                    keynodes[CommonIdentifiers.RREL_DYNAMIC_ARGUMENT.value],
                    keynodes[rrel_identifier],
                )
                ctx.CreateEdge(ScType.EdgeAccessConstPosTemp, variable, argument)
            else:
                generate_binary_relation(
                    ctx, action, ScType.EdgeAccessConstPosPerm, argument, keynodes[rrel_identifier]
                )

    return action


def generate_action(ctx: ScMemoryContext, concepts: list) -> ScAddr:
    action = ctx.CreateNode(ScType.NodeConst)
    keynodes = GlobalScKeynodes(ctx)
    for concept in concepts:
        ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, keynodes[concept], action)

    return action


def generate_initiated_action(ctx: ScMemoryContext, arguments: dict, concepts: list) -> ScAddr:
    keynodes = GlobalScKeynodes(ctx)

    action = generate_action_with_arguments(ctx, arguments, concepts)
    ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, keynodes[CommonIdentifiers.QUESTION_INITIATED.value], action)

    return action


def generate_message_decomposition(ctx: ScMemoryContext, message: ScAddr, atomic_messages_list: list) -> None:
    keynodes = GlobalScKeynodes(ctx)

    decomposition_tuple = "_decomposition_tuple"

    template = ScTemplate()

    template.TripleWithRelation(
        ScType.NodeVarTuple >> decomposition_tuple,
        ScType.EdgeDCommonVar,
        message,
        ScType.EdgeAccessVarPosPerm,
        keynodes[MessageIdentifiers.NREL_MESSAGE_DECOMPOSITION.value],
    )

    is_first = True
    previous_message = None
    for atomic_message in atomic_messages_list:
        if is_first:
            template.TripleWithRelation(
                decomposition_tuple,
                ScType.EdgeAccessVarPosPerm,
                atomic_message,
                ScType.EdgeAccessVarPosPerm,
                keynodes[CommonIdentifiers.RREL_ONE.value],
            )
            is_first = False
        else:
            template.Triple(decomposition_tuple, ScType.EdgeAccessVarPosPerm, atomic_message)
            template.TripleWithRelation(
                previous_message,
                ScType.EdgeDCommonVar,
                atomic_message,
                ScType.EdgeAccessVarPosPerm,
                keynodes[MessageIdentifiers.NREL_MESSAGE_SEQUENCE.value],
            )
        previous_message = atomic_message

    template_params = ScTemplateParams()
    ctx.HelperGenTemplate(template, template_params)


def generate_result(
    ctx: ScMemoryContext,
    arguments: dict,
    concepts: list,
    initiation=CommonIdentifiers.QUESTION_INITIATED,
    reaction=CommonIdentifiers.QUESTION_FINISHED_UNSUCCESSFULLY,
    wait_time=COMMON_WAIT_TIME,
) -> bool:
    keynodes = GlobalScKeynodes(ctx)
    question = generate_action_with_arguments(ctx, arguments, concepts)
    ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, keynodes[initiation.value], question)

    wait_agent(ctx, wait_time, question, keynodes[CommonIdentifiers.QUESTION_FINISHED.value])
    result = ctx.HelperCheckEdge(keynodes[reaction.value], question, ScType.EdgeAccessConstPosPerm)
    return result


def generate_formed_message(
    ctx: ScMemoryContext, text=None, tokens=None, link_classes=None, message_classes=None
) -> ScAddr:
    keynodes = GlobalScKeynodes(ctx)

    if text is not None:
        text_link = generate_link(ctx, text)
    else:
        text_link = ctx.CreateLink()

    if tokens is not None:
        generate_decomposition_into_tokens(ctx, keynodes, text_link, tokens)

    message = generate_message(ctx, {text_link: link_classes})

    if message_classes is not None:
        for message_class in message_classes:
            message_class_node = keynodes[message_class]
            if message_class_node.IsValid():
                ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, message_class_node, message)
    return message
