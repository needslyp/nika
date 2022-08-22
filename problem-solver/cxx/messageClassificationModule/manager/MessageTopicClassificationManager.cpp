/*
 * Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
 * Author Maksim Orlov
 */

#include "manager/MessageTopicClassificationManager.hpp"

#include "client/WitAiClient.hpp"

namespace messageClassificationModule
{
MessageTopicClassificationManager::MessageTopicClassificationManager(ScMemoryContext * context)
{
  classifier = std::make_unique<MessageTopicClassifier>(context, new WitAiClient());
}

ScAddrVector MessageTopicClassificationManager::manage(ScAddrVector const & processParameters) const
{
  ScAddr messageAddr = processParameters.at(0);
  ScAddrVector answerElements = classifier->classifyMessage(messageAddr);

  return answerElements;
}

}  // namespace messageClassificationModule
