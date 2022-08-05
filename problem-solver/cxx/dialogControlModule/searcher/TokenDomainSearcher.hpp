/*
* Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
*/

#pragma once

#include "sc-memory/sc_addr.hpp"
#include "keynodes/CoreKeynodes.hpp"
#include "handler/LinkHandler.hpp"

namespace dialogControlModule
{
class TokenDomainSearcher
{
public:
  explicit TokenDomainSearcher(ScMemoryContext * ms_context);

  ~TokenDomainSearcher();

  ScAddr getMessageText(const ScAddr & message);

private:
  ScMemoryContext * context;
  commonModule::LinkHandler * linkHandler;
};
}
