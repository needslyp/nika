/*
 * Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
 * Author Maksim Orlov
 */

#include "sc-config/sc_config.hpp"

#include "WitAiClient.hpp"

messageClassificationModule::WitAiClient::WitAiClient()
{
  ScConfig config{MESSAGE_CLASSIFICATION_CONFIG_PATH};
  ScConfigGroup group{config["wit-ai"]};
  witAiServerToken = group["server_token"];
  witAiUrl = group["url"];
}

json messageClassificationModule::WitAiClient::getWitResponse(std::string const & messageText)
{
  auto response = cpr::Get(cpr::Url{witAiUrl}, cpr::Bearer{witAiServerToken}, cpr::Parameters{{"q", messageText}});

  return json::parse(response.text);
}
