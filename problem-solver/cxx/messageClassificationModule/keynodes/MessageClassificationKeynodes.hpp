/*
 * Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
 * Author Maksim Orlov
 */

#pragma once

#include "sc-memory/sc_addr.hpp"
#include "sc-memory/sc_object.hpp"

#include "MessageClassificationKeynodes.generated.hpp"

namespace messageClassificationModule
{
class MessageClassificationKeynodes : public ScObject
{
  SC_CLASS()
  SC_GENERATED_BODY()

public:
  SC_PROPERTY(Keynode("action_message_topic_classification"), ForceCreate)
  static ScAddr action_message_topic_classification;

  SC_PROPERTY(Keynode("concept_intent_possible_class"), ForceCreate)
  static ScAddr concept_intent_possible_class;

  SC_PROPERTY(Keynode("concept_trait_possible_class"), ForceCreate)
  static ScAddr concept_trait_possible_class;

  SC_PROPERTY(Keynode("concept_entity_possible_class"), ForceCreate)
  static ScAddr concept_entity_possible_class;

  SC_PROPERTY(Keynode("nrel_wit_ai_idtf"), ForceCreate)
  static ScAddr nrel_wit_ai_idtf;

  SC_PROPERTY(Keynode("nrel_entity_possible_role"), ForceCreate)
  static ScAddr nrel_entity_possible_role;
};

}  // namespace messageClassificationModule
