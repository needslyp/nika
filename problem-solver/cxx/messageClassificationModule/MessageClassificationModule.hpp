/*
 * Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
 * Author Maksim Orlov
 */

#pragma once

#include "sc-memory/sc_module.hpp"

#include "MessageClassificationModule.generated.hpp"

namespace messageClassificationModule
{
class MessageClassificationModule : public ScModule
{
  SC_CLASS(LoadOrder(100))
  SC_GENERATED_BODY()

  sc_result InitializeImpl() override;

  sc_result ShutdownImpl() override;
};

}  // namespace messageClassificationModule
