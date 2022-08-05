"""
    Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
    Author Nikiforov Sergei
"""

from common import ScKeynodes
from common_module.constant.identifiers import CommonIdentifiers, TokenIdentifiers
from sc import ScAddr, ScMemoryContext, ScType


def generate_decomposition_into_tokens(ctx: ScMemoryContext, keynodes: ScKeynodes, link: ScAddr, tokens: list) -> None:
    tuple_node = ctx.CreateNode(ScType.NodeConstTuple)
    concatenation_edge = ctx.CreateEdge(ScType.EdgeDCommonConst, tuple_node, link)
    ctx.CreateEdge(
        ScType.EdgeAccessConstPosPerm,
        keynodes[TokenIdentifiers.NREL_DECOMPOSITION_INTO_TOKENS.value],
        concatenation_edge,
    )
    previous_decomposition_access_link = None
    for token in tokens:
        token_link = ctx.CreateLink()
        ctx.SetLinkContent(token_link, token)
        decomposition_access_link = ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, tuple_node, token_link)
        if previous_decomposition_access_link is not None:
            sequence_arc = ctx.CreateEdge(
                ScType.EdgeDCommonConst, previous_decomposition_access_link, decomposition_access_link
            )
            ctx.CreateEdge(
                ScType.EdgeAccessConstPosPerm, keynodes[TokenIdentifiers.NREL_TOKEN_SEQUENCE.value], sequence_arc
            )
        else:
            ctx.CreateEdge(
                ScType.EdgeAccessConstPosPerm, keynodes[CommonIdentifiers.RREL_ONE.value], decomposition_access_link
            )
        previous_decomposition_access_link = decomposition_access_link
