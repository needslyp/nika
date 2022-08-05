"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from common.sc_log import Log
from common_module.constant.identifiers import CommonIdentifiers, LangIdentifiers
from common_module.exception.custom_exception import CustomException
from common_module.keynode.global_sc_keynodes import GlobalScKeynodes
from sc import ScAddr, ScMemoryContext, ScTemplate, ScType
from text_to_speech_module.constant.synthesizer_identifiers import SynthesizerIdentifiers
from text_to_speech_module.creator.voice_creator import create_voice


def get_system_synthesizer(ctx: ScMemoryContext) -> ScAddr:
    synthesizer = "_synthesizer"

    keynodes = GlobalScKeynodes(ctx)
    template = ScTemplate()
    template.TripleWithRelation(
        keynodes[CommonIdentifiers.MYSELF.value],
        ScType.EdgeDCommonVar,
        ScType.NodeVar >> synthesizer,
        ScType.EdgeAccessVarPosPerm,
        keynodes[SynthesizerIdentifiers.NREL_SYNTHESIZER.value],
    )
    template.Triple(
        keynodes[SynthesizerIdentifiers.CONCEPT_SYNTHESIZER.value], ScType.EdgeAccessVarPosPerm, synthesizer
    )
    search_result = ctx.HelperSearchTemplate(template)
    search_result_size = search_result.Size()
    if search_result_size == 1:
        synthesizer_node = search_result[0][synthesizer]
    else:
        raise CustomException("Unable to find a synthesizer because no ScStructures were found.")

    return synthesizer_node


def get_current_synthesizer_voices(ctx: ScMemoryContext, synthesizer: ScAddr) -> dict:
    if not synthesizer.IsValid():
        raise CustomException("The synthesizer ScAddr isn't valid.")

    log = Log(get_current_synthesizer_voices.__name__)
    set_parameter = "_set"
    voice_parameter = "_voice"

    voices = {}

    keynodes = GlobalScKeynodes(ctx)
    template = ScTemplate()
    template.TripleWithRelation(
        synthesizer,
        ScType.EdgeDCommonVar,
        ScType.NodeVar >> set_parameter,
        ScType.EdgeAccessVarPosPerm,
        keynodes[SynthesizerIdentifiers.NREL_CURRENT_VOICES.value],
    )
    template.Triple(set_parameter, ScType.EdgeAccessVarPosPerm, ScType.NodeVar >> voice_parameter)

    search_result = ctx.HelperSearchTemplate(template)
    search_result_size = search_result.Size()
    if search_result_size == 0:
        raise CustomException("No ScStructures were found.")

    for i in range(0, search_result_size):
        voice_node = search_result[i][voice_parameter]
        try:
            voice = create_voice(ctx, voice_node)
            lang = voice.lang.value
            if lang != LangIdentifiers.LANG_NONE.value:
                voices[lang] = voice
        except CustomException as ex:
            log.warning(str(ex))

    return voices
