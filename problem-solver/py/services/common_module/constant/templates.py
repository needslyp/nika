"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Alexandr Zagorskiy
"""

from enum import Enum

from common import ScAddr, ScKeynodes, ScTemplate, ScType
from common_module.constant.identifiers import CommonIdentifiers


class CommonTemplates:
    @staticmethod
    def deactivated_action_template(keynodes: ScKeynodes, action: str):
        action = keynodes[action]
        action_deactivated = keynodes[CommonIdentifiers.ACTION_DEACTIVATED.value]
        templ = ScTemplate()
        templ.Triple(action_deactivated, ScType.EdgeAccessVarPosPerm, action)
        return templ

    @staticmethod
    def input_action_template(keynodes: ScKeynodes, action: str, action_node: ScAddr) -> ScTemplate:
        action = keynodes[action]

        action_templ = ScTemplate()
        action_templ.Triple(action, ScType.EdgeAccessVarPosPerm, action_node)
        return action_templ

    @staticmethod
    def action_status_template(keynodes: ScKeynodes, action_node: ScAddr, is_success=True) -> ScTemplate:
        quest_finish = keynodes[CommonIdentifiers.QUESTION_FINISHED.value]
        if is_success:
            quest_finish_res = keynodes[CommonIdentifiers.QUESTION_FINISHED_SUCCESSFULLY.value]
        else:
            quest_finish_res = keynodes[CommonIdentifiers.QUESTION_FINISHED_UNSUCCESSFULLY.value]

        action_templ = ScTemplate()
        action_templ.Triple(quest_finish, ScType.EdgeAccessVarPosPerm, action_node)
        action_templ.Triple(quest_finish_res, ScType.EdgeAccessVarPosPerm, action_node)
        return action_templ

    @staticmethod
    def dynamic_argument_template(keynodes: ScKeynodes, action_node: ScAddr, rrel: ScAddr) -> ScTemplate:
        rrel_dyn_arg = keynodes[CommonIdentifiers.RREL_DYNAMIC_ARGUMENT.value]

        templ = ScTemplate()
        templ.TripleWithRelation(
            action_node,
            ScType.EdgeAccessVarPosPerm >> CommonTemplateVarNames.DYNAMIC_ARGUMENT_ACCESS_ARC.value,
            ScType.NodeVar >> CommonTemplateVarNames.DYNAMIC_ARGUMENT.value,
            ScType.EdgeAccessVarPosPerm,
            rrel,
        )
        templ.Triple(
            rrel_dyn_arg, ScType.EdgeAccessVarPosPerm, CommonTemplateVarNames.DYNAMIC_ARGUMENT_ACCESS_ARC.value
        )
        return templ

    @staticmethod
    def dynamic_argument_value_template(keynodes: ScKeynodes, action_node: ScAddr, rrel: ScAddr) -> ScTemplate:
        templ = CommonTemplates.dynamic_argument_template(keynodes, action_node, rrel)
        templ.Triple(
            CommonTemplateVarNames.DYNAMIC_ARGUMENT.value,
            ScType.EdgeAccessVarPosTemp,
            ScType.NodeVar >> CommonTemplateVarNames.DYNAMIC_ARGUMENT_VALUE.value,
        )
        return templ

    @staticmethod
    def triple_with_relation_template(node: ScAddr, is_begin, relation: ScAddr, is_role: bool) -> ScTemplate:
        arc_type = ScType.EdgeAccessVarPosPerm if is_role else ScType.EdgeDCommonVar

        templ = ScTemplate()
        if is_begin:
            templ.TripleWithRelation(
                node,
                arc_type,
                ScType.NodeVar >> CommonTemplateVarNames.SEARCH_BY_RELATION_RESULT.value,
                ScType.EdgeAccessVarPosPerm,
                relation,
            )
        else:
            templ.TripleWithRelation(
                ScType.NodeVar >> CommonTemplateVarNames.SEARCH_BY_RELATION_RESULT.value,
                arc_type,
                node,
                ScType.EdgeAccessVarPosPerm,
                relation,
            )
        return templ


class CommonTemplateVarNames(Enum):
    LANG = "_lang"
    DYNAMIC_ARGUMENT = "_dynamic_argument"
    DYNAMIC_ARGUMENT_VALUE = "_dynamic_argument_value"
    SEARCH_BY_RELATION_RESULT = "_search_by_relation_result"
    DYNAMIC_ARGUMENT_ACCESS_ARC = "_dynamic_argument_access_arc"
