/*
 * Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
 * Author Dzmitry Brutski
 */

#include <utility>
#include <fstream>

#include "config.hpp"

using namespace std;

Config::Config(std::string fileName)
    : m_fileName(std::move(fileName))
{
}
string getValue(const string & line, const string & key)
{
  string value = "";
  if (line.find(key) != std::string::npos)
  {
    value = line.substr(line.find('=') + 1);
    while (value.find(' ') != std::string::npos)
    {
      value = value.substr(value.find(' ') + 1);
    }
  }
  return value;
}
std::string Config::getByKey(const string & key)
{
  string value;
  string line;
  ifstream cfg(m_fileName);
  if (cfg.is_open())
  {
    while (getline(cfg, line))
    {
      value = getValue(line, key);
      if (!value.empty())
        return value;
    }
  }
}
