/*
 * Copyright (c) 2022 Intelligent Semantic Systems LLC, All rights reserved.
 * Author Maksim Orlov
 */

#include "MessageClassificationKeynodes.hpp"

#include "sc-memory/sc_memory.hpp"

namespace messageClassificationModule
{
ScAddr MessageClassificationKeynodes::action_message_topic_classification;
ScAddr MessageClassificationKeynodes::concept_intent_possible_class;
ScAddr MessageClassificationKeynodes::concept_trait_possible_class;
ScAddr MessageClassificationKeynodes::concept_entity_possible_class;
ScAddr MessageClassificationKeynodes::nrel_wit_ai_idtf;
ScAddr MessageClassificationKeynodes::nrel_entity_possible_role;

}  // namespace messageClassificationModule
