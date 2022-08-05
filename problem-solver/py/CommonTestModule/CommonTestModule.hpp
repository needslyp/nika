/*
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Alexandr Zagorskiy
*/

#pragma once

#include <sc-memory/sc_module.hpp>

#include "CommonTestService.hpp"
#include "CommonTestModule.generated.hpp"


class CommonTestModule : public ScModule
{
  SC_CLASS(LoadOrder(200))
  SC_GENERATED_BODY()

  virtual sc_result InitializeImpl() override;
  virtual sc_result ShutdownImpl() override;

private:
  std::unique_ptr<CommonTestPythonService> m_commonTestPythonService;
};
