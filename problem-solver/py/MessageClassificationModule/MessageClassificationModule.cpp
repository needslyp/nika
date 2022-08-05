/*
* Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
* Author Nikiforov Sergei
*/

#include "MessageClassificationModule.hpp"

SC_IMPLEMENT_MODULE(MessageClassificationModule)

sc_result MessageClassificationModule::InitializeImpl()
{
  m_messageClassificationPythonService.reset(new MessageClassificationPythonService(
        "message_classification_module/message_classification_module.py"));
  m_messageClassificationPythonService->Run();
  return SC_RESULT_OK;
}

sc_result MessageClassificationModule::ShutdownImpl()
{
  m_messageClassificationPythonService->Stop();
  m_messageClassificationPythonService.reset();
  return SC_RESULT_OK;
}
