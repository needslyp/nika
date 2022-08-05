/*
* Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
* Author Orlov Maksim
*/

#include <sc-agents-common/utils/AgentUtils.hpp>
#include "sc-agents-common/utils/IteratorUtils.hpp"

#include "keynodes/Keynodes.hpp"
#include "keynodes/MessageReplyKeynodes.hpp"

#include "GenerateErrorReplyMessageAgent.hpp"

using namespace messageReplyModuleTest;

SC_AGENT_IMPLEMENTATION(GenerateErrorReplyMessageAgent)
{
  ScAddr actionAddr = m_memoryCtx.GetEdgeTarget(edgeAddr);
  if(!m_memoryCtx.HelperCheckEdge(
        commonModule::Keynodes::action_interpret_non_atomic_action, actionAddr, ScType::EdgeAccessConstPosPerm))
  {
    return SC_RESULT_OK;
  }

  if(!actionIsValid(actionAddr))
  {
    utils::AgentUtils::finishAgentWork(&m_memoryCtx, actionAddr, false);
  }

  ScAddr argsSet = utils::IteratorUtils::getFirstByOutRelation(
        & m_memoryCtx,
        actionAddr,
        scAgentsCommon::CoreKeynodes::rrel_2);
  ScAddr messageAddr = utils::IteratorUtils::getFirstByOutRelation(
        & m_memoryCtx,
        argsSet,
        scAgentsCommon::CoreKeynodes::rrel_1);

  ScTemplate scTemplate;
  scTemplate.TripleWithRelation(
      messageAddr,
      ScType::EdgeDCommonVar,
      ScType::NodeVar,
      ScType::EdgeAccessVarPosPerm,
      messageReplyModule::MessageReplyKeynodes::nrel_reply);
  ScTemplateGenResult templateGenResult;
  m_memoryCtx.HelperGenTemplate(scTemplate, templateGenResult);

  utils::AgentUtils::finishAgentWork(&m_memoryCtx, actionAddr, true);
  return SC_RESULT_OK;
}

bool GenerateErrorReplyMessageAgent::actionIsValid(ScAddr const & actionAddr)
{
  std::string const MESSAGE_ALIAS = "_message";
  std::string const ARGS_SET_ALIAS = "_args_set";

  ScTemplate actionTemplate;
  actionTemplate.TripleWithRelation(
        actionAddr,
        ScType::EdgeAccessVarPosPerm,
        messageReplyModule::MessageReplyKeynodes::error_message_processing_program,
        ScType::EdgeAccessVarPosPerm,
        scAgentsCommon::CoreKeynodes::rrel_1);
  actionTemplate.TripleWithRelation(
        actionAddr,
        ScType::EdgeAccessVarPosPerm,
        ScType::NodeVar >> ARGS_SET_ALIAS,
        ScType::EdgeAccessVarPosPerm,
        scAgentsCommon::CoreKeynodes::rrel_2);
  actionTemplate.TripleWithRelation(
        ARGS_SET_ALIAS,
        ScType::EdgeAccessVarPosPerm,
        ScType::NodeVar >> MESSAGE_ALIAS,
        ScType::EdgeAccessVarPosPerm,
        scAgentsCommon::CoreKeynodes::rrel_1);
  actionTemplate.Triple(
        messageReplyModule::MessageReplyKeynodes::concept_message,
        ScType::EdgeAccessVarPosPerm,
        MESSAGE_ALIAS);
  actionTemplate.Triple(
          messageReplyModule::MessageReplyKeynodes::concept_error_message,
          ScType::EdgeAccessVarPosPerm,
          MESSAGE_ALIAS);
  ScTemplateSearchResult searchResult;
  m_memoryCtx.HelperSearchTemplate(actionTemplate, searchResult);
  return searchResult.Size() == 1;
}
