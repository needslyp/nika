/*
 * Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
 * Author Maksim Orlov
 */

#pragma once

#include "sc-memory/sc_memory.hpp"
#include "sc-memory/sc_addr.hpp"

#include "classifier/MessageTopicClassifier.hpp"

namespace messageClassificationModule
{
class MessageTopicClassificationManager
{
public:
  explicit MessageTopicClassificationManager(ScMemoryContext * context);

  ScAddrVector manage(ScAddrVector const & processParameters) const;

protected:
  std::unique_ptr<MessageTopicClassifier> classifier;
};

}  // namespace messageClassificationModule
