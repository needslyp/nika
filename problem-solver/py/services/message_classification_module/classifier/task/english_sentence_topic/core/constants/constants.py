"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Mikhno Egor
"""

from enum import Enum


class Headers(Enum):
    AUTHORIZATION = "authorization"
    CONTENT_TYPE = "content-type"


class Intent(Enum):
    ID = "id"
    NAME = "name"
    ENTITIES = "entities"
    TRAITS = "traits"


class IntentAction(Enum):
    ADD_INTENT = "add_intent"


class Entity(Enum):
    ID = Intent.ID.value
    NAME = Intent.NAME.value
    ROLES = "roles"
    LOOKUPS = "lookups"
    KEYWORDS = "keywords"


class EntityAction(Enum):
    ADD_ENTITY = "add_entity"
    ADD_ROLES = "add_roles"
    ADD_KEYWORDS = "add_keywords"
    ADD_SYNONYMS = "add_synonyms"


class EntityRoles(Enum):
    ID = Intent.ID.value
    NAME = Intent.NAME.value


class EntityLookups(Enum):
    KEYWORDS = Entity.KEYWORDS.value
    FREE_TEXT = "free-text"


class EntityKeywords(Enum):
    KEYWORD = "keyword"
    SYNONYMS = "synonyms"


class EntitySynonym(Enum):
    KEYWORD = EntityKeywords.KEYWORD.value
    SYNONYM = "synonym"


class Trait(Enum):
    ID = Intent.ID.value
    NAME = Intent.NAME.value
    VALUES = "values"


class TraitAction(Enum):
    ADD_TRAIT = "add_trait"
    ADD_VALUES = "add_values"


class TraitValue(Enum):
    ID = Intent.ID.value
    VALUE = "value"


class UtteranceIntent(Enum):
    INTENT = "intent"


class UtteranceEntity(Enum):
    ENTITY = "entity"
    START = "start"
    END = "end"
    BODY = "body"
    ENTITIES = Intent.ENTITIES.value


class UtteranceTrait(Enum):
    TRAIT = "trait"
    VALUE = TraitValue.VALUE.value


class Utterance(Enum):
    TEXT = "text"
    INTENT = UtteranceIntent.INTENT.value
    ENTITIES = UtteranceEntity.ENTITIES.value
    TRAITS = Intent.TRAITS.value


UNKNOWN = "unknown"
