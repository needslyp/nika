/*
 * Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
 * Author Maksim Orlov
 */

#include "WitAiClient.hpp"

#include "sc-config/sc_config.hpp"
#include "sc-memory/utils/sc_log.hpp"

messageClassificationModule::WitAiClient::WitAiClient()
{
  ScConfig config{MESSAGE_CLASSIFICATION_CONFIG_PATH};
  ScConfigGroup group{config["wit-ai"]};
  witAiServerToken = group["server_token"];
  witAiUrl = group["url"];
}

json messageClassificationModule::WitAiClient::getWitResponse(std::string const & messageText)
{
  json jsonResponse;
  try
  {
    auto response = cpr::Get(cpr::Url{witAiUrl}, cpr::Bearer{witAiServerToken}, cpr::Parameters{{"q", messageText}});
    jsonResponse = json::parse(response.text);
  }
  catch (...)
  {
    SC_LOG_ERROR("WitAiClient: Internet connection error.");
  }

  return jsonResponse;
}
