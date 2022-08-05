/*
* Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
* Author Nikiforov Sergei
*/

#pragma once

#include <sc-memory/sc_module.hpp>

#include "MessageClassificationService.hpp"
#include "MessageClassificationModule.generated.hpp"


class MessageClassificationModule : public ScModule
{
  SC_CLASS(LoadOrder(100))
  SC_GENERATED_BODY()

  virtual sc_result InitializeImpl() override;
  virtual sc_result ShutdownImpl() override;

private:
  std::unique_ptr<MessageClassificationPythonService> m_messageClassificationPythonService;
};
