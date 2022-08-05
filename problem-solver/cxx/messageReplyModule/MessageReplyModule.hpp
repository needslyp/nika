/*
* Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
* Author Nikiforov Sergei
*/

#pragma once

#include "sc-memory/sc_memory.hpp"
#include "sc-memory/sc_module.hpp"

#include "keynodes/MessageReplyKeynodes.hpp"
#include "agent/MessageReplyAgent.hpp"
#include "agent/ErrorMessageReplyAgent.hpp"
#include "utils/ActionUtils.hpp"

#include "MessageReplyModule.generated.hpp"

namespace messageReplyModule
{

class MessageReplyModule : public ScModule
{
  SC_CLASS(LoadOrder(100))
  SC_GENERATED_BODY()

  virtual sc_result

  InitializeImpl() override;

  virtual sc_result ShutdownImpl() override;
};

}
