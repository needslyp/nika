/*
* Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
* Author Ruslan Korshunov
*/


#pragma once

#include "sc-memory/sc_module.hpp"
#include "SpeechToTextService.hpp"
#include "SpeechToTextModule.generated.hpp"


class SpeechToTextModule : public ScModule
{
  SC_CLASS(LoadOrder(100))
  SC_GENERATED_BODY()

  virtual sc_result InitializeImpl() override;
  virtual sc_result ShutdownImpl() override;

private:
  std::unique_ptr<SpeechToTextPythonService> m_SpeechToTextService;
};
