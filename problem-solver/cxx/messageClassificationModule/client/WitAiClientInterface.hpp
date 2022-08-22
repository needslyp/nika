/*
 * Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
 * Author Maksim Orlov
 */

#pragma once

#include <nlohmann/json.hpp>

using json = nlohmann::json;

namespace messageClassificationModule
{
class WitAiClientInterface
{
public:
  virtual json getWitResponse(std::string const & messageText) = 0;

  virtual ~WitAiClientInterface() = default;
};

}  // namespace messageClassificationModule
