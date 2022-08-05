/*
* Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
* Author Ruslan Korshunov
*/

#include "SpeechToTextModule.hpp"

SC_IMPLEMENT_MODULE(SpeechToTextModule)

sc_result SpeechToTextModule::InitializeImpl()
{
  m_SpeechToTextService.reset(
        new SpeechToTextPythonService("speech_to_text_module/speech_to_text_module.py"));
  m_SpeechToTextService->Run();
  return SC_RESULT_OK;
}

sc_result SpeechToTextModule::ShutdownImpl()
{
  m_SpeechToTextService->Stop();
  m_SpeechToTextService.reset();
  return SC_RESULT_OK;
}
