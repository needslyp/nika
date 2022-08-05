"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from common_module.constant.identifiers import CommonIdentifiers, MessageIdentifiers
from common_module.constant.templates import CommonTemplates, CommonTemplateVarNames
from common_module.keynode.global_sc_keynodes import GlobalScKeynodes
from sc import ScAddr, ScMemoryContext, ScTemplateParams, ScType


def generate_binary_relation(
    ctx: ScMemoryContext, first_node: ScAddr, edge: ScType, second_node: ScAddr, *relations: ScAddr
) -> ScAddr:
    main_edge = ctx.CreateEdge(edge, first_node, second_node)
    for relation in relations:
        ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, relation, main_edge)
    return main_edge


def generate_link(ctx: ScMemoryContext, link_content) -> ScAddr:
    link = None
    if link_content != "" and link_content is not None:
        link = ctx.CreateLink()
        ctx.SetLinkContent(link, link_content)
    return link


def generate_action_node_construction(ctx: ScMemoryContext, action: str, action_node: ScAddr) -> None:
    action_template = CommonTemplates.input_action_template(GlobalScKeynodes(ctx), action, action_node)
    action_params = ScTemplateParams()
    ctx.HelperGenTemplate(action_template, action_params)


def generate_action_status(ctx: ScMemoryContext, action_node: ScAddr, is_success: bool) -> None:
    action_template = CommonTemplates.action_status_template(GlobalScKeynodes(ctx), action_node, is_success)
    action_params = ScTemplateParams()
    ctx.HelperGenTemplate(action_template, action_params)


def generate_dynamic_argument(ctx: ScMemoryContext, action_node: ScAddr) -> None:
    rrel_2 = GlobalScKeynodes(ctx)[CommonIdentifiers.RREL_TWO.value]
    dyn_arg_node = ctx.CreateNode(ScType.NodeConst)
    dyn_arg_template = CommonTemplates.dynamic_argument_template(GlobalScKeynodes(ctx), action_node, rrel_2)
    dyn_arg_params = ScTemplateParams()
    dyn_arg_params.Add(CommonTemplateVarNames.DYNAMIC_ARGUMENT.value, dyn_arg_node)
    ctx.HelperGenTemplate(dyn_arg_template, dyn_arg_params)


def generate_dynamic_argument_value(ctx: ScMemoryContext, action_node: ScAddr, argument_value_node: ScAddr) -> None:
    rrel_2 = GlobalScKeynodes(ctx)[CommonIdentifiers.RREL_TWO.value]
    template = CommonTemplates.dynamic_argument_template(GlobalScKeynodes(ctx), action_node, rrel_2)
    search_res = ctx.HelperSearchTemplate(template)
    dyn_arg_node = search_res[0][CommonTemplateVarNames.DYNAMIC_ARGUMENT.value]
    ctx.CreateEdge(ScType.EdgeAccessConstPosTemp, dyn_arg_node, argument_value_node)


def generate_message(ctx: ScMemoryContext, links: dict) -> ScAddr:
    keynodes = GlobalScKeynodes(ctx)

    message = ctx.CreateNode(ScType.NodeConst)
    text_translation_node = ctx.CreateNode(ScType.NodeConst)

    ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, keynodes[MessageIdentifiers.CONCEPT_MESSAGE.value], message)
    generate_binary_relation(
        ctx,
        text_translation_node,
        ScType.EdgeDCommonConst,
        message,
        keynodes[CommonIdentifiers.NREL_SC_TEXT_TRANSLATION.value],
    )
    for link in links:
        ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, text_translation_node, link)
        for concept in links[link]:
            ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, keynodes[concept], link)

    return message
