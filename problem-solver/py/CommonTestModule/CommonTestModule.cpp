/*
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Alexandr Zagorskiy
*/

#include "CommonTestModule.hpp"

SC_IMPLEMENT_MODULE(CommonTestModule)

sc_result CommonTestModule::InitializeImpl()
{
  m_commonTestPythonService.reset(new CommonTestPythonService(
        "common_module/test_module/common_test_module.py"));
  m_commonTestPythonService->Run();
  return SC_RESULT_OK;
}

sc_result CommonTestModule::ShutdownImpl()
{
  m_commonTestPythonService->Stop();
  m_commonTestPythonService.reset();
  return SC_RESULT_OK;
}
