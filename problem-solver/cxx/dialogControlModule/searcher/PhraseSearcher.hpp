/*
* Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
* Author Ruslan Korshunov
*/

#include <vector>

#include "sc-memory/sc_addr.hpp"
#include "sc-memory/sc_memory.hpp"

namespace dialogControlModule
{
class PhraseSearcher
{
public:
  explicit PhraseSearcher(ScMemoryContext * ms_context);

  std::vector<ScAddr> getPhrases(const ScAddr & phraseClassNode, const ScAddr & langNode);

  ScAddr getFirstPhraseClass(const ScAddr & logicRuleNode);

  ScAddr getNextPhraseClass(const ScAddr & phraseClassNode);
private:
  ScMemoryContext * context;
};
}
