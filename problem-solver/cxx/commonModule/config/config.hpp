/*
 * Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
 * Author Dzmitry Brutski
 */
#pragma once

#include <string>

class Config
{
  std::string m_fileName;

public:
  explicit Config(std::string fileName);
  std::string getByKey(const std::string & key);
};
