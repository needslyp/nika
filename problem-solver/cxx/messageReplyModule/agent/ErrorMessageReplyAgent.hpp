/*
* Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
* Author Maksim Orlov
*/

#pragma once

#include "sc-memory/kpm/sc_agent.hpp"
#include "sc-agents-common/keynodes/coreKeynodes.hpp"

#include "ErrorMessageReplyAgent.generated.hpp"

namespace messageReplyModule
{

class ErrorMessageReplyAgent : public ScAgent
{
  SC_CLASS(Agent, Event(scAgentsCommon::CoreKeynodes::question_initiated, ScEvent::Type::AddOutputEdge))
  SC_GENERATED_BODY()

private:
  int WAIT_TIME = 5000;

  bool checkActionClass(ScAddr const & actionAddr);

  ScAddr getMessageProcessingProgram();

  ScAddr generateNonAtomicActionArgsSet(ScAddr const & messageAddr);

  ScAddr generateAnswer(ScAddr const & messageAddr);

  bool waitForActionSuccessfulFinish(ScAddr const & actionAddr);
};

} // namespace messageReplyModule
