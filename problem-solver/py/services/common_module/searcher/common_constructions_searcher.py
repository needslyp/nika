"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from common_module.constant.extension import AUDIO_FORMATS, AudioExtension
from common_module.constant.identifiers import CommonIdentifiers, FormatIdentifiers, LangIdentifiers, MessageIdentifiers
from common_module.constant.messages import CustomExceptionMessages
from common_module.constant.templates import CommonTemplates, CommonTemplateVarNames
from common_module.exception.custom_exception import CustomException
from common_module.keynode.global_sc_keynodes import GlobalScKeynodes
from sc import ScAddr, ScMemoryContext, ScTemplate, ScType


def get_action_argument(ctx: ScMemoryContext, question: ScAddr, rrel: str, argument_class=None) -> ScAddr:
    actual_argument = "_actual_argument"
    argument_node = get_argument_as_dynamic(ctx, question, rrel, argument_class)

    if argument_node is None:
        keynodes = GlobalScKeynodes(ctx)

        template = ScTemplate()
        template.TripleWithRelation(
            question,
            ScType.EdgeAccessVarPosPerm,
            ScType.NodeVar >> actual_argument,
            ScType.EdgeAccessVarPosPerm,
            keynodes[rrel],
        )
        if argument_class is not None:
            template.Triple(keynodes[argument_class], ScType.EdgeAccessVarPosPerm, actual_argument)

        search_result = ctx.HelperSearchTemplate(template)

        search_result_size = search_result.Size()
        if search_result_size > 0:
            argument_node = search_result[0][actual_argument]
        else:
            raise CustomException("The argument node isn't found.")

    return argument_node


def get_argument_as_dynamic(ctx: ScMemoryContext, question: ScAddr, rrel: str, argument_class=None):
    argument_node = None
    keynodes = GlobalScKeynodes(ctx)

    template = CommonTemplates.dynamic_argument_value_template(keynodes, question, keynodes[rrel])

    if argument_class is not None:
        template.Triple(
            keynodes[argument_class], ScType.EdgeAccessVarPosPerm, CommonTemplateVarNames.DYNAMIC_ARGUMENT_VALUE.value
        )

    search_result = ctx.HelperSearchTemplate(template)
    if search_result.Size() > 0:
        argument_node = search_result[0][CommonTemplateVarNames.DYNAMIC_ARGUMENT_VALUE.value]

    return argument_node


def get_message_link_list(ctx: ScMemoryContext, message: ScAddr, link_concepts=None) -> ScAddr:
    if not message.IsValid():
        raise CustomException("The message ScAddr isn't valid.")

    text_translation = "_text_translation"
    link = "_link"

    keynodes = GlobalScKeynodes(ctx)

    template = ScTemplate()
    template.TripleWithRelation(
        ScType.NodeVar >> text_translation,
        ScType.EdgeDCommonVar,
        message,
        ScType.EdgeAccessVarPosPerm,
        keynodes[CommonIdentifiers.NREL_SC_TEXT_TRANSLATION.value],
    )
    template.Triple(text_translation, ScType.EdgeAccessVarPosPerm, ScType.LinkVar >> link)
    if link_concepts is not None:
        for concept in link_concepts:
            node_addr = keynodes[concept]
            if node_addr.IsValid():
                template.Triple(node_addr, ScType.EdgeAccessVarPosPerm, link)
    search_result = ctx.HelperSearchTemplate(template)
    search_result_size = search_result.Size()

    link_list = []

    if search_result_size > 0:
        for index in range(0, search_result_size):
            link_list.append(search_result[index][link])
    return link_list


def get_message_link(ctx: ScMemoryContext, message: ScAddr, link_concepts=None) -> ScAddr:
    link_node = None
    link_list = get_message_link_list(ctx, message, link_concepts)

    if len(link_list) > 0:
        link_node = link_list[0]
    return link_node


def is_action_deactivated(ctx: ScMemoryContext, action: str) -> bool:
    template = CommonTemplates.deactivated_action_template(GlobalScKeynodes(ctx), action)
    search_res = ctx.HelperSearchTemplate(template)
    return bool(search_res.Size())


def is_action_node_valid(ctx: ScMemoryContext, action: str, action_node: ScAddr) -> bool:
    template = CommonTemplates.input_action_template(GlobalScKeynodes(ctx), action, action_node)
    search_res = ctx.HelperSearchTemplate(template)
    return bool(search_res.Size())


def get_edge(ctx: ScMemoryContext, src: ScAddr, trg: ScAddr) -> ScAddr:
    iter_faf = ctx.Iterator3(src, ScType.EdgeAccessConstPosPerm, trg)
    edge = iter_faf.Get(1)
    return edge


def get_dynamic_argument(ctx: ScMemoryContext, question: ScAddr, rrel: str):
    message_node = None
    keynodes = GlobalScKeynodes(ctx)
    template = CommonTemplates.dynamic_argument_template(keynodes, question, keynodes[rrel])
    search_result = ctx.HelperSearchTemplate(template)
    if search_result.Size() > 0:
        message_node = search_result[0][CommonTemplateVarNames.DYNAMIC_ARGUMENT.value]

    return message_node


def get_link_language_class(ctx: ScMemoryContext, link: ScAddr) -> str:
    lang = "_lang"

    keynodes = GlobalScKeynodes(ctx)

    template = ScTemplate()
    template.Triple(ScType.NodeVar >> lang, ScType.EdgeAccessVarPosPerm, link)
    template.Triple(keynodes[LangIdentifiers.LANGUAGES.value], ScType.EdgeAccessVarPosPerm, lang)

    search_result = ctx.HelperSearchTemplate(template)
    search_result_size = search_result.Size()

    if search_result_size == 0:
        raise CustomException("The link language isn't specified.")

    return ctx.HelperGetSystemIdtf(search_result[0][lang])


def get_audio_format(ctx: ScMemoryContext, link: ScAddr) -> str:
    audio_format = "_format"

    keynodes = GlobalScKeynodes(ctx)

    template = ScTemplate()
    template.Triple(ScType.NodeVar >> audio_format, ScType.EdgeAccessVarPosPerm, link)
    template.Triple(keynodes[FormatIdentifiers.FORMAT_AUDIO.value], ScType.EdgeAccessVarPosPerm, audio_format)

    search_result = ctx.HelperSearchTemplate(template)
    search_result_size = search_result.Size()

    if search_result_size > 0:
        format_class = ctx.HelperGetSystemIdtf(search_result[0][audio_format])
        format_value = AUDIO_FORMATS[format_class]
        if format_value == AudioExtension.NOT_SETTED:
            raise CustomException('The audio format "{}" isn\'t supported by the agent.'.format(format_class))
    else:
        raise CustomException("The audio format isn't specified.")

    return format_value


def get_message_link_language(ctx: ScMemoryContext, message: ScAddr) -> str:
    text_link = get_message_link(ctx, message, [CommonIdentifiers.CONCEPT_TEXT_FILE.value])
    if text_link is None:
        raise CustomException("Message text link is not found.")
    return get_link_language_class(ctx, text_link)


def get_message_decomposition(ctx: ScMemoryContext, message: ScAddr) -> list:
    decomposition_tuple = "_decomposition_tuple"
    atomic_message = "_atomic_message"

    keynodes = GlobalScKeynodes(ctx)

    template = ScTemplate()
    template.TripleWithRelation(
        ScType.NodeVarTuple >> decomposition_tuple,
        ScType.EdgeDCommonVar,
        message,
        ScType.EdgeAccessVarPosPerm,
        keynodes[MessageIdentifiers.NREL_MESSAGE_DECOMPOSITION.value],
    )
    template.Triple(decomposition_tuple, ScType.EdgeAccessVarPosPerm, ScType.NodeVar >> atomic_message)
    search_result = ctx.HelperSearchTemplate(template)
    search_result_size = search_result.Size()
    if search_result_size > 0:
        atomic_messages_list = []
        for index in range(0, search_result_size):
            atomic_messages_list.append(search_result[index][atomic_message])
    else:
        raise CustomException(CustomExceptionMessages.DECOMPOSITION_NOT_FOUND.value)

    return atomic_messages_list


def get_language_list(ctx: ScMemoryContext) -> list:
    languages = list()
    template = ScTemplate()
    language = "_language"
    template.Triple(
        GlobalScKeynodes(ctx)[LangIdentifiers.LANGUAGES.value], ScType.EdgeAccessVarPosPerm, ScType.NodeVar >> language
    )
    result = ctx.HelperSearchTemplate(template)
    for i in range(result.Size()):
        languages.append(result[i][language])
    return languages
