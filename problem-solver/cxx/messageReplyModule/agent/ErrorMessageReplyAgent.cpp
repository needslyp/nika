/*
* Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
* Author Orlov Maksim
*/

#include "sc-agents-common/utils/AgentUtils.hpp"
#include "sc-agents-common/utils/IteratorUtils.hpp"
#include "sc-agents-common/keynodes/coreKeynodes.hpp"
#include "utils/ActionUtils.hpp"
#include "keynodes/Keynodes.hpp"

#include "keynodes/MessageReplyKeynodes.hpp"

#include "ErrorMessageReplyAgent.hpp"

using namespace messageReplyModule;
using namespace scAgentsCommon;

SC_AGENT_IMPLEMENTATION(ErrorMessageReplyAgent)
{
  ScAddr actionAddr = otherAddr;
  if (!checkActionClass(actionAddr))
  {
    return SC_RESULT_OK;
  }

  SC_LOG_DEBUG("ErrorMessageReplyAgent started")

  ScAddr errorMessage = utils::IteratorUtils::getFirstByOutRelation(&m_memoryCtx, actionAddr, CoreKeynodes::rrel_1);
  ScAddr processingProgramAddr = getMessageProcessingProgram();

  if (!errorMessage.IsValid())
  {
    SC_LOG_ERROR("Message processing program not found.")
    utils::AgentUtils::finishAgentWork(&m_memoryCtx, actionAddr, false);
    return SC_RESULT_ERROR;
  }
  if (!processingProgramAddr.IsValid())
  {
    SC_LOG_ERROR("Message processing program not found.")
    utils::AgentUtils::finishAgentWork(&m_memoryCtx, actionAddr, false);
    return SC_RESULT_ERROR;
  }

  ScAddrVector argsVector = {processingProgramAddr, generateNonAtomicActionArgsSet(errorMessage)};
  ScAddr actionToInterpret = utils::AgentUtils::initAgent(
      &m_memoryCtx,
      commonModule::Keynodes::action_interpret_non_atomic_action,
      argsVector);
  if (!waitForActionSuccessfulFinish(actionToInterpret))
  {
    SC_LOG_ERROR("Error action wait time expired or action not finished successfully")
    if (!waitForActionSuccessfulFinish(actionToInterpret))
    {
      throw std::runtime_error("ErrorMessageReplyAgent: Error reply message not generated");
    }
  }
  ScAddr answerAddr;
  try
  {
    answerAddr = generateAnswer(errorMessage);
  }
  catch (std::runtime_error & exception)
  {
    SC_LOG_ERROR(exception.what())
    utils::AgentUtils::finishAgentWork(&m_memoryCtx, actionAddr, false);
    return SC_RESULT_ERROR;
  }

  SC_LOG_DEBUG("ErrorMessageReplyAgent finished")
  utils::AgentUtils::finishAgentWork(&m_memoryCtx, actionAddr, answerAddr, true);
  return SC_RESULT_OK;
}

bool ErrorMessageReplyAgent::checkActionClass(ScAddr const & actionAddr)
{
  return m_memoryCtx.HelperCheckEdge(MessageReplyKeynodes::action_reply_to_error_message, actionAddr, ScType::EdgeAccessConstPosPerm);
}

ScAddr ErrorMessageReplyAgent::getMessageProcessingProgram()
{
  return MessageReplyKeynodes::error_message_processing_program;
}

ScAddr ErrorMessageReplyAgent::generateNonAtomicActionArgsSet(ScAddr const & messageAddr)
{
  const std::string ARGS_SET_ALIAS = "_args_set";

  ScTemplate actionArgsTemplate;
  actionArgsTemplate.TripleWithRelation(
      ScType::NodeVar >> ARGS_SET_ALIAS,
      ScType::EdgeAccessVarPosPerm,
      messageAddr,
      ScType::EdgeAccessVarPosPerm,
      CoreKeynodes::rrel_1);

  ScTemplateGenResult templateGenResult;
  if (!m_memoryCtx.HelperGenTemplate(actionArgsTemplate, templateGenResult))
  {
    throw std::runtime_error("Unable to generate arguments set for interpreter agent action");
  }
  return templateGenResult[ARGS_SET_ALIAS];
}

ScAddr ErrorMessageReplyAgent::generateAnswer(ScAddr const & messageAddr)
{
  const std::string ANSWER_STRUCT_ALIAS = "_answer";
  const std::string REPLY_MESSAGE_ALIAS = "_reply_message";
  const std::string REPLY_MESSAGE_RELATION_PAIR_ARC = "_reply_message_relation_pair_arc";
  const std::string REPLY_MESSAGE_RELATION_ACCESS_ARC = "_reply_message_relation_access_arc";

  ScTemplate replySearchTemplate;
  replySearchTemplate.TripleWithRelation(
      messageAddr,
      ScType::EdgeDCommonVar >> REPLY_MESSAGE_RELATION_PAIR_ARC,
      ScType::NodeVar >> REPLY_MESSAGE_ALIAS,
      ScType::EdgeAccessVarPosPerm >> REPLY_MESSAGE_RELATION_ACCESS_ARC,
      MessageReplyKeynodes::nrel_reply);
  ScTemplateSearchResult searchResult;
  m_memoryCtx.HelperSearchTemplate(replySearchTemplate, searchResult);
  m_memoryCtx.CreateNode(ScType::NodeConstStruct);
  ScTemplate answerGenerationTemplate;
  answerGenerationTemplate.Triple(
      ScType::NodeVarStruct >> ANSWER_STRUCT_ALIAS,
      ScType::EdgeAccessVarPosPerm,
      messageAddr);
    answerGenerationTemplate.Triple(
            ANSWER_STRUCT_ALIAS,
            ScType::EdgeAccessVarPosPerm,
            searchResult[0][REPLY_MESSAGE_RELATION_PAIR_ARC]);
    answerGenerationTemplate.Triple(
            ANSWER_STRUCT_ALIAS,
            ScType::EdgeAccessVarPosPerm,
            searchResult[0][REPLY_MESSAGE_ALIAS]);
    answerGenerationTemplate.Triple(
            ANSWER_STRUCT_ALIAS,
            ScType::EdgeAccessVarPosPerm,
            searchResult[0][REPLY_MESSAGE_RELATION_ACCESS_ARC]);
    answerGenerationTemplate.Triple(
            ANSWER_STRUCT_ALIAS,
            ScType::EdgeAccessVarPosPerm,
            MessageReplyKeynodes::nrel_reply);

  ScAddrVector classes;
  ScAddrVector classesArcs;
  ScIterator3Ptr classesIt = m_memoryCtx.Iterator3(
    ScType::NodeConstClass,
    ScType::EdgeAccessConstPosPerm,
    messageAddr
  );

  while (classesIt->Next())
  {
    classes.emplace_back(classesIt->Get(0));
    classesArcs.emplace_back(classesIt->Get(1));
  }

  for (size_t i = 0; i < classes.size(); i++)
  {
    answerGenerationTemplate.Triple(
      ANSWER_STRUCT_ALIAS,
      ScType::EdgeAccessVarPosPerm,
      classes.at(i)
      );
    answerGenerationTemplate.Triple(
      ANSWER_STRUCT_ALIAS,
      ScType::EdgeAccessVarPosPerm,
      classesArcs.at(i)
      );
  }

  ScTemplateGenResult templateGenResult;
  if (!m_memoryCtx.HelperGenTemplate(answerGenerationTemplate, templateGenResult))
  {
    throw std::runtime_error("Unable to generate answer.");
  }
  return templateGenResult[ANSWER_STRUCT_ALIAS];
}

bool ErrorMessageReplyAgent::waitForActionSuccessfulFinish(ScAddr const & actionAddr)
{
  return ActionUtils::waitAction(&m_memoryCtx, actionAddr, WAIT_TIME) &&
      m_memoryCtx.HelperCheckEdge(
          CoreKeynodes::question_finished_successfully,
          actionAddr,
          ScType::EdgeAccessConstPosPerm);
}
