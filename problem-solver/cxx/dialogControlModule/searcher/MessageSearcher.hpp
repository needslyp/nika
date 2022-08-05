/*
* Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
* Author Ruslan Korshunov
*/

#pragma once

#include "sc-memory/sc_addr.hpp"
#include "sc-memory/sc_memory.hpp"

namespace dialogControlModule
{
class MessageSearcher
{
public:
  explicit MessageSearcher(ScMemoryContext * ms_context);

  ScAddr getFirstMessage(const ScAddr & nonAtomicMessageNode);

  ScAddr getNextMessage(const ScAddr & messageNode);

  ScAddr getMessageAuthor(const ScAddr & messageNode);

  ScAddr getMessageTheme(const ScAddr & messageNode);

private:
  ScMemoryContext * context;
};
}
