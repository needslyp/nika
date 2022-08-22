/*
 * Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
 * Author Maksim Orlov
 */

#pragma once

#include "gmock/gmock.h"

#include "client/WitAiClientInterface.hpp"

namespace messageClassificationModule
{
class WitAiClientMock : public WitAiClientInterface
{
public:
  MOCK_METHOD(json, getWitResponse, (std::string const & messageText), (override));
};

}  // namespace messageClassificationModule
