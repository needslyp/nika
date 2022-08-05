/*
* Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
* Author Ruslan Korshunov
*/

#include "TextToSpeechModule.hpp"

SC_IMPLEMENT_MODULE(TextToSpeechModule)

sc_result TextToSpeechModule::InitializeImpl()
{
  m_TextToSpeechService.reset(
        new TextToSpeechPythonService("text_to_speech_module/text_to_speech_module.py"));
  m_TextToSpeechService->Run();
  return SC_RESULT_OK;
}

sc_result TextToSpeechModule::ShutdownImpl()
{
  m_TextToSpeechService->Stop();
  m_TextToSpeechService.reset();
  return SC_RESULT_OK;
}
