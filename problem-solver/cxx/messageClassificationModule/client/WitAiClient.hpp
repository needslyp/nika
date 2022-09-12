/*
 * Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
 * Author Maksim Orlov
 */

#pragma once

#include <memory>

#include "client/WitAiClientInterface.hpp"

namespace messageClassificationModule
{
class WitAiClient : public WitAiClientInterface
{
public:
  WitAiClient();

  json getWitResponse(std::string const & messageText) override;

  ~WitAiClient() override = default;

protected:
  std::string witAiServerToken;

  std::string witAiUrl;
};

}  // namespace messageClassificationModule
