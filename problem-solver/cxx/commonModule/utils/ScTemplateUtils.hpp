/*
* Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
*/

#pragma once

#include "sc-memory/sc_addr.hpp"
#include "sc-memory/sc_template.hpp"
#include "sc-memory/sc_memory.hpp"

class ScTemplateUtils
{
public:
  static ScAddrVector getAllWithKey(ScMemoryContext * context, const ScTemplate & scTemplate, const std::string & key);
};
