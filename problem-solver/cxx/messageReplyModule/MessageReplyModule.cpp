/*
* Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
* Author Nikiforov Sergei
*/

#include "MessageReplyModule.hpp"

using namespace messageReplyModule;

SC_IMPLEMENT_MODULE(MessageReplyModule)

sc_result MessageReplyModule::InitializeImpl()
{
  if (!messageReplyModule::MessageReplyKeynodes::InitGlobal())
  {
    return SC_RESULT_ERROR;
  }

  ScMemoryContext ctx(sc_access_lvl_make_min, "MessageReplyModule");
  if (ActionUtils::isActionDeactivated(&ctx, MessageReplyKeynodes::action_reply_to_message))
  {
    SC_LOG_ERROR("action_reply_to_message is deactivated");
  }
  else 
  {
    SC_AGENT_REGISTER(MessageReplyAgent);
  }

  if (ActionUtils::isActionDeactivated(&ctx, MessageReplyKeynodes::action_reply_to_error_message))
  {
    SC_LOG_ERROR("action_reply_to_error_message is deactivated");
  }
  else
  {
    SC_AGENT_REGISTER(ErrorMessageReplyAgent);
  }

  return SC_RESULT_OK;
}

sc_result MessageReplyModule::ShutdownImpl()
{
  SC_AGENT_UNREGISTER(MessageReplyAgent);
  SC_AGENT_UNREGISTER(ErrorMessageReplyAgent);

  return SC_RESULT_OK;
}
