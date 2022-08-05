/*
* Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
* Author Alexandr Zagorskiy
*/

#pragma once

#include "sc-memory/sc_memory.hpp"
#include "sc-memory/sc_module.hpp"

#include "keynodes/Keynodes.hpp"
#include "agent/NonAtomicActionInterpreterAgent.hpp"

#include "CommonModule.generated.hpp"
#include "utils/ActionUtils.hpp"

namespace commonModule
{

class CommonModule : public ScModule
{
  SC_CLASS(LoadOrder(100))
  SC_GENERATED_BODY()

  virtual sc_result

  InitializeImpl() override;

  virtual sc_result ShutdownImpl() override;
};

}
