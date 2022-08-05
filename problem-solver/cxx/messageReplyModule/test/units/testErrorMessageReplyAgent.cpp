/*
* Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
* Author Orlov Maksim
*/

#include "sc_test.hpp"
#include "builder/src/scs_loader.hpp"
#include "sc-memory/kpm/sc_agent.hpp"
#include "sc-memory/sc_wait.hpp"
#include "sc-agents-common/keynodes/coreKeynodes.hpp"
#include "agent/ErrorMessageReplyAgent.hpp"
#include "keynodes/Keynodes.hpp"
#include "keynodes/MessageReplyKeynodes.hpp"
#include "test/agent/GenerateErrorReplyMessageAgent.hpp"
#include "utils/ActionUtils.hpp"

namespace errorMessageReplyModuleTest
{
ScsLoader loader;
const std::string TEST_FILES_DIR_PATH = MESSAGE_REPLY_MODULE_TEST_SRC_PATH "/testStructures/";
const int WAIT_TIME = 5000;

using ErrorMessageReplyAgentTest = ScMemoryTest;

void initialize()
{
  scAgentsCommon::CoreKeynodes::InitGlobal();
  commonModule::Keynodes::InitGlobal();
  messageReplyModule::MessageReplyKeynodes::InitGlobal();

  ScAgentInit(true);
  SC_AGENT_REGISTER(messageReplyModule::ErrorMessageReplyAgent)
}

void shutdown()
{
  SC_AGENT_UNREGISTER(messageReplyModule::ErrorMessageReplyAgent)
}

TEST_F(ErrorMessageReplyAgentTest, errorMessageReplySuccessful)
{
  ScMemoryContext & context = *m_ctx;

  loader.loadScsFile(context,TEST_FILES_DIR_PATH + "errorReplyMessageAgentTestStructure.scs");
  initialize();
  SC_AGENT_REGISTER(messageReplyModuleTest::GenerateErrorReplyMessageAgent)

  ScAddr test_action_node = context.HelperFindBySystemIdtf("test_action_node");
  EXPECT_TRUE(test_action_node.IsValid());

  context.CreateEdge(
          ScType::EdgeAccessConstPosPerm,
          scAgentsCommon::CoreKeynodes::question_initiated,
          test_action_node);

  EXPECT_TRUE(ActionUtils::waitAction(&context, test_action_node, WAIT_TIME));
  EXPECT_TRUE(context.HelperCheckEdge(
          scAgentsCommon::CoreKeynodes::question_finished_successfully,
          test_action_node,
          ScType::EdgeAccessConstPosPerm));

  SC_AGENT_UNREGISTER(messageReplyModuleTest::GenerateErrorReplyMessageAgent)
  shutdown();
}

}//namespace errorMessageReplyModuleTest
