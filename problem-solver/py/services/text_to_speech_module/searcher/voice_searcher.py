"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from common_module.constant.identifiers import CommonIdentifiers, LangIdentifiers
from common_module.exception.custom_exception import CustomException
from common_module.keynode.global_sc_keynodes import GlobalScKeynodes
from sc import ScAddr, ScMemoryContext, ScTemplate, ScType
from text_to_speech_module.constant.synthesizer_constants import SYNTHESIZERS, VOICES_SEX, Sex, Synthesizers
from text_to_speech_module.constant.synthesizer_identifiers import (
    VOICES_CLASSES_BY_LANGUAGE,
    VOICES_CLASSES_BY_SEX,
    SynthesizerIdentifiers,
)


def get_synthesizer(ctx: ScMemoryContext, voice: ScAddr) -> Synthesizers:
    if not voice.IsValid():
        raise CustomException("The voice ScAddr isn't valid.")

    synthesizer = Synthesizers.NOT_SETTED

    keynodes = GlobalScKeynodes(ctx)

    for voice_class in SYNTHESIZERS.keys():
        template = ScTemplate()
        template.Triple(keynodes[voice_class], ScType.EdgeAccessVarPosPerm, voice)

        search_result = ctx.HelperSearchTemplate(template)
        search_result_size = search_result.Size()

        if search_result_size == 1:
            synthesizer = SYNTHESIZERS[voice_class]
            break

    if synthesizer == Synthesizers.NOT_SETTED:
        raise CustomException("The voice's synthesizer isn't found.")

    return synthesizer


def get_sex(ctx: ScMemoryContext, voice: ScAddr) -> Sex:
    if not voice.IsValid():
        raise CustomException("The voice ScAddr isn't valid.")

    keynodes = GlobalScKeynodes(ctx)

    sex = Sex.NOT_SETTED

    for voice_class in VOICES_CLASSES_BY_SEX:
        template = ScTemplate()
        template.Triple(keynodes[voice_class], ScType.EdgeAccessVarPosPerm, voice)

        search_result = ctx.HelperSearchTemplate(template)
        search_result_size = search_result.Size()
        if search_result_size == 1:
            if voice_class in VOICES_SEX.keys():
                sex = VOICES_SEX[voice_class]
            break

    if sex == Sex.NOT_SETTED:
        raise CustomException("The voice's sex isn't found.")

    return sex


def get_voice_id(ctx: ScMemoryContext, voice: ScAddr) -> str:
    if not voice.IsValid():
        raise CustomException("The voice ScAddr isn't valid.")

    link = "_link"

    keynodes = GlobalScKeynodes(ctx)

    template = ScTemplate()
    template.TripleWithRelation(
        voice,
        ScType.EdgeDCommonVar,
        ScType.LinkVar >> link,
        ScType.EdgeAccessVarPosPerm,
        keynodes[SynthesizerIdentifiers.NREL_VOICE_ID.value],
    )

    search_result = ctx.HelperSearchTemplate(template)
    search_result_size = search_result.Size()

    if search_result_size == 1:
        link_node = search_result[0][link]
        voice_id = ctx.GetLinkContent(link_node).AsString()
    else:
        raise CustomException("The voice's identifier isn't found.")

    return voice_id


def get_voice_language(ctx: ScMemoryContext, voice: ScAddr) -> str:
    if not voice.IsValid():
        raise CustomException("The voice ScAddr isn't valid.")

    lang_class = "_lang_class"
    lang = LangIdentifiers.LANG_NONE

    keynodes = GlobalScKeynodes(ctx)
    for voice_class in VOICES_CLASSES_BY_LANGUAGE:
        template = ScTemplate()
        template.Triple(keynodes[voice_class], ScType.EdgeAccessVarPosPerm, voice)
        template.TripleWithRelation(
            keynodes[voice_class],
            ScType.EdgeDCommonVar,
            ScType.NodeVarClass >> lang_class,
            ScType.EdgeAccessVarPosPerm,
            keynodes[CommonIdentifiers.NREL_VOICE_LANGUAGE.value],
        )

        search_result = ctx.HelperSearchTemplate(template)
        search_result_size = search_result.Size()
        if search_result_size == 1:
            lang_idtf = ctx.HelperGetSystemIdtf(search_result[0][lang_class])
            values = [item.value for item in LangIdentifiers]
            if lang_idtf not in values:
                raise CustomException("The found voice language identifier is unknown.")
            lang = LangIdentifiers(lang_idtf)
            break

    if lang == LangIdentifiers.LANG_NONE:
        lang = get_voice_language_by_dialect(ctx, voice)

    return lang


def get_voice_language_by_dialect(ctx: ScMemoryContext, voice: ScAddr) -> str:
    if not voice.IsValid():
        raise CustomException("The voice ScAddr isn't valid.")

    class_parameter = "_class"
    lang_class = "_lang_class"
    lang = LangIdentifiers.LANG_NONE

    keynodes = GlobalScKeynodes(ctx)
    for voice_class in VOICES_CLASSES_BY_LANGUAGE:
        template = ScTemplate()
        template.Triple(ScType.NodeVarClass >> class_parameter, ScType.EdgeAccessVarPosPerm, voice)
        template.TripleWithRelation(
            keynodes[voice_class],
            ScType.EdgeDCommonVar,
            class_parameter,
            ScType.EdgeAccessVarPosPerm,
            keynodes[CommonIdentifiers.NREL_INCLUSION.value],
        )
        template.TripleWithRelation(
            keynodes[voice_class],
            ScType.EdgeDCommonVar,
            ScType.NodeVarClass >> lang_class,
            ScType.EdgeAccessVarPosPerm,
            keynodes[CommonIdentifiers.NREL_VOICE_LANGUAGE.value],
        )

        search_result = ctx.HelperSearchTemplate(template)
        search_result_size = search_result.Size()
        if search_result_size == 1:
            lang_idtf = ctx.HelperGetSystemIdtf(search_result[0][lang_class])
            values = [item.value for item in LangIdentifiers]
            if lang_idtf not in values:
                raise CustomException("The found voice language identifier is unknown.")
            lang = LangIdentifiers(lang_idtf)
            break

    if lang == LangIdentifiers.LANG_NONE:
        raise CustomException("The voice lang isn't found.")

    return lang


def check_affiliation(ctx: ScMemoryContext, voice: ScAddr, class_identifier: SynthesizerIdentifiers) -> bool:
    if not voice.IsValid():
        raise CustomException("The voice ScAddr isn't valid.")

    keynodes = GlobalScKeynodes(ctx)

    result = False
    template = ScTemplate()
    template.Triple(keynodes[class_identifier.value], ScType.EdgeAccessVarPosPerm, voice)

    search_result = ctx.HelperSearchTemplate(template)
    search_result_size = search_result.Size()
    if search_result_size == 1:
        result = True

    return result
