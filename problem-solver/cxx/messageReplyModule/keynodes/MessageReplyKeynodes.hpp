/*
* Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
* Author Nikiforov Sergei
*/

#pragma once

#include "sc-memory/sc_addr.hpp"
#include "sc-memory/sc_object.hpp"

#include "MessageReplyKeynodes.generated.hpp"

namespace messageReplyModule
{

class MessageReplyKeynodes : public ScObject
{
  SC_CLASS()
  SC_GENERATED_BODY()

public:
  SC_PROPERTY(Keynode("action_reply_to_message"), ForceCreate)
  static ScAddr action_reply_to_message;

  SC_PROPERTY(Keynode("message_processing_program"), ForceCreate)
  static ScAddr message_processing_program;

  SC_PROPERTY(Keynode("nrel_authors"), ForceCreate)
  static ScAddr nrel_authors;

  SC_PROPERTY(Keynode("concept_message"), ForceCreate)
  static ScAddr concept_message;

  SC_PROPERTY(Keynode("nrel_reply"), ForceCreate)
  static ScAddr nrel_reply;

  SC_PROPERTY(Keynode("format_wav"), ForceCreate)
  static ScAddr format_wav;

  SC_PROPERTY(Keynode("languages"), ForceCreate)
  static ScAddr languages;

  SC_PROPERTY(Keynode("concept_sound_file"), ForceCreate)
  static ScAddr concept_sound_file;

  SC_PROPERTY(Keynode("concept_text_file"), ForceCreate)
  static ScAddr concept_text_file;

  SC_PROPERTY(Keynode("concept_error_message"), ForceCreate)
  static ScAddr concept_error_message;

  SC_PROPERTY(Keynode("action_reply_to_error_message"), ForceCreate)
  static ScAddr action_reply_to_error_message;

  SC_PROPERTY(Keynode("error_message_processing_program"), ForceCreate)
  static ScAddr error_message_processing_program;
};

} // namespace messageReplyModule
