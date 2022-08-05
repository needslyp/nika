/*
* Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
* Author Orlov Maksim
*/

#pragma once

#include "sc-memory/kpm/sc_agent.hpp"
#include "keynodes/MessageReplyKeynodes.hpp"
#include "sc-agents-common/keynodes/coreKeynodes.hpp"

#include "GenerateErrorReplyMessageAgent.generated.hpp"

namespace messageReplyModuleTest
{

class GenerateErrorReplyMessageAgent : public ScAgent
{
  SC_CLASS(Agent, Event(scAgentsCommon::CoreKeynodes::question_initiated, ScEvent::Type::AddOutputEdge))
  SC_GENERATED_BODY()

private:
  bool actionIsValid(ScAddr const & actionAddr);
};

} // namespace commonTest
