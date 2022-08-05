/*
* Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
* Author Ruslan Korshunov
*/


#pragma once

#include "sc-memory/sc_module.hpp"
#include "TextToSpeechService.hpp"
#include "TextToSpeechModule.generated.hpp"


class TextToSpeechModule : public ScModule
{
  SC_CLASS(LoadOrder(100))
  SC_GENERATED_BODY()

  virtual sc_result InitializeImpl() override;
  virtual sc_result ShutdownImpl() override;

private:
  std::unique_ptr<TextToSpeechPythonService> m_TextToSpeechService;
};
