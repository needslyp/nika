/*
 * Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
 * Author Maksim Orlov
 */

#include "config/config.hpp"

#include "WitAiClient.hpp"

messageClassificationModule::WitAiClient::WitAiClient()
{
  Config config(MESSAGE_CLASSIFICATION_CONFIG_PATH);
  witAiServerToken = config.getByKey("WitAiServerToken");
  witAiUrl = config.getByKey("WitAiUrl");
}

json messageClassificationModule::WitAiClient::getWitResponse(std::string const & messageText)
{
  auto response = cpr::Get(cpr::Url{witAiUrl}, cpr::Bearer{witAiServerToken}, cpr::Parameters{{"q", messageText}});

  return json::parse(response.text);
}
