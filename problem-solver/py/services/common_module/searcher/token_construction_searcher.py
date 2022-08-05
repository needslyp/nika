"""
    Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
    Author Nikiforov Sergei
"""

from common_module.constant.identifiers import TokenIdentifiers, CommonIdentifiers
from common_module.exception.custom_exception import CustomException
from common_module.keynode.global_sc_keynodes import GlobalScKeynodes
from sc import ScAddr, ScMemoryContext, ScTemplate, ScType


def get_token_class_by_language(ctx: ScMemoryContext, language: str) -> ScAddr:
    keynodes = GlobalScKeynodes(ctx)

    token_class = "_token_class"

    template = ScTemplate()
    template.TripleWithRelation(
        ScType.NodeVar >> token_class,
        ScType.EdgeDCommonVar,
        keynodes[language],
        ScType.EdgeAccessVarPosPerm,
        keynodes[TokenIdentifiers.NREL_TOKEN_LANGUAGE.value],
    )
    search_result = ctx.HelperSearchTemplate(template)

    if search_result.Size() != 1:
        raise CustomException("A language for the token class is not found or several languages are found.")

    return search_result[0][token_class]


def get_decomposition_tuple(ctx: ScMemoryContext, link: ScAddr) -> ScAddr:
    keynodes = GlobalScKeynodes(ctx)

    decomposition_tuple = None

    decomposition_tuple_alias = "_decomposition_tuple"

    template = ScTemplate()

    template.TripleWithRelation(
        ScType.NodeVar >> decomposition_tuple_alias,
        ScType.EdgeDCommonVar,
        link,
        ScType.EdgeAccessVarPosPerm,
        keynodes[TokenIdentifiers.NREL_DECOMPOSITION_INTO_TOKENS.value],
    )

    search_results = ctx.HelperSearchTemplate(template)
    if search_results.Size() == 1:
        decomposition_tuple = search_results[0][decomposition_tuple_alias]
    return decomposition_tuple


def get_first_link_from_decomposition(ctx: ScMemoryContext, decomposition_tuple: ScAddr) -> ScAddr:
    keynodes = GlobalScKeynodes(ctx)

    first_link = None

    first_link_alias = "_first_link"

    template = ScTemplate()

    template.TripleWithRelation(
        decomposition_tuple,
        ScType.EdgeAccessVarPosPerm,
        ScType.LinkVar >> first_link_alias,
        ScType.EdgeAccessVarPosPerm,
        keynodes[CommonIdentifiers.RREL_ONE.value],
    )

    search_results = ctx.HelperSearchTemplate(template)
    if search_results.Size() == 1:
        first_link = search_results[0][first_link_alias]
    return first_link


def get_next_link_from_decomposition(ctx: ScMemoryContext, decomposition_tuple: ScAddr, link: ScAddr) -> ScAddr:
    keynodes = GlobalScKeynodes(ctx)

    next_link = None

    next_link_alias = "_next_link"
    current_link_access_arc = "_current_link_access_arc"
    next_link_access_arc = "_next_link_access_arc"
    template = ScTemplate()

    template.Triple(decomposition_tuple, ScType.EdgeAccessVarPosPerm >> current_link_access_arc, link)
    template.Triple(
        decomposition_tuple, ScType.EdgeAccessVarPosPerm >> next_link_access_arc, ScType.LinkVar >> next_link_alias
    )
    template.TripleWithRelation(
        current_link_access_arc,
        ScType.EdgeDCommonVar,
        next_link_access_arc,
        ScType.EdgeAccessVarPosPerm,
        keynodes[TokenIdentifiers.NREL_TOKEN_SEQUENCE.value],
    )

    search_result = ctx.HelperSearchTemplate(template)
    if search_result.Size() == 1:
        next_link = search_result[0][next_link_alias]
    return next_link
