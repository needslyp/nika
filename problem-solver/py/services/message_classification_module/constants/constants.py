"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Nikiforov Sergei
Author Kseniya Bantsevich
Author Anastasiya Vasilevskaya
"""

from enum import Enum
from common_module.constant.identifiers import CommonIdentifiers


ARGUMENT_THRESHOLD = 0


class ResponseConstants(Enum):
    ENTITIES = "entities"
    CONFIDENCE = "confidence"
    VALUE = "value"
    NORMALIZED = "normalized"
    TRAITS = "traits"
    BODY = "body"
    INTENTS = "intents"
    NAME = "name"


class Idtf(Enum):
    NREL_WIT_AI_IDTF = "nrel_wit_ai_idtf"
    NREL_ENTITY_POSSIBLE_ROLE = "nrel_entity_possible_role"
    CONCEPT_ENTITY_POSSIBLE_CLASS = "concept_entity_possible_class"
    CONCEPT_TRAIT_POSSIBLE_CLASS = "concept_trait_possible_class"
    CONCEPT_INTENT_POSSIBLE_CLASS = "concept_intent_possible_class"
    RREL_ENTITY = "rrel_entity"
    NREL_SURNAME = "nrel_surname"
    NREL_NAME = "nrel_name"
    NREL_MIDDLE_NAME = "nrel_middle_name"


class WitEntities(Enum):
    FEELING = "feeling"
    HEALTH_STATE = "health_state"
    SEASON = "season"
    WIT_CONTACT = "wit$contact"
    WIT_DATETIME = "wit$datetime"
    WIT_TEMPERATURE = "wit$temperature"


class WitRoles(Enum):
    FEELING = "feeling"
    HEALTH_STATE = "health_state"
    SEASON = "season"
    CONTACT = "contact"
    DATETIME = "datetime"
    TEMPERATURE = "temperature"


MODULE_NAME = "MessageClassificationModule"

IDTFS_FOR_SEARCH = [
    CommonIdentifiers.NREL_MAIN_IDTF.value,
    CommonIdentifiers.NREL_IDTF.value,
    Idtf.NREL_NAME.value,
    Idtf.NREL_SURNAME.value,
    Idtf.NREL_MIDDLE_NAME.value,
]
