"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from common_module.constant.identifiers import CommonIdentifiers
from common_module.exception.custom_exception import CustomException
from common_module.keynode.global_sc_keynodes import GlobalScKeynodes
from sc import ScAddr, ScMemoryContext, ScTemplate, ScType
from speech_to_text_module.constant.recognizer_constants import RecognizerIdentifiers


def get_system_recognizer(ctx: ScMemoryContext) -> ScAddr:
    recognizer = "_recognizer"
    keynodes = GlobalScKeynodes(ctx)
    template = ScTemplate()
    template.TripleWithRelation(
        keynodes[CommonIdentifiers.MYSELF.value],
        ScType.EdgeDCommonVar,
        ScType.NodeVar >> recognizer,
        ScType.EdgeAccessVarPosPerm,
        keynodes[RecognizerIdentifiers.NREL_RECOGNIZER.value],
    )
    template.Triple(keynodes[RecognizerIdentifiers.CONCEPT_RECOGNIZER.value], ScType.EdgeAccessVarPosPerm, recognizer)
    search_result = ctx.HelperSearchTemplate(template)
    search_result_size = search_result.Size()
    if search_result_size == 1:
        recognizer_node = search_result[0][recognizer]
    else:
        raise CustomException("Unable to find a recognizer because no ScStructures were found.")

    return recognizer_node
