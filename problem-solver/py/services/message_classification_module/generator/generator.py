"""
    Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
    Author Anastasiya Vasilevskaya
"""

from common import ScAddr, ScMemoryContext, ScType, ScTemplate
from common_module.generator.common_constructions_generator import generate_binary_relation


def generate_message_specification(
    ctx: ScMemoryContext,
    message_node: ScAddr,
    message_classes: list,
    entities: list,
    rrel_entity: ScAddr,
    contour: ScAddr,
) -> None:
    for message_class in message_classes:
        edge = ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, message_class, message_node)
        ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, message_class)
        ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, edge)

    for entity in entities:
        main_edge = generate_binary_relation(
            ctx,
            message_node,
            ScType.EdgeAccessConstPosPerm,
            entity,
            rrel_entity,
        )
        template = ScTemplate()
        template.TripleWithRelation(
            message_node,
            main_edge,
            entity,
            ScType.EdgeAccessVarPosPerm >> "_edge",
            rrel_entity,
        )
        ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, entity)
        ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, rrel_entity)
        ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, main_edge)
        result = ctx.HelperSearchTemplate(template)
        if result.Size() > 0:
            for i in range(result.Size()):
                ctx.CreateEdge(ScType.EdgeAccessConstPosPerm, contour, result[i]["_edge"])
