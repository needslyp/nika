"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Nikiforov Sergei
Author Kseniya Bantsevich
Author Anastasiya Vasilevskaya
"""

from enum import Enum


class MessageTypeClasses(Enum):
    pass


class ClassificationIdentifiers(Enum):
    ACTION_MESSAGE_TOPIC_CLASSIFICATION = "action_message_topic_classification"


class WitRolesIdentifiers(Enum):
    RREL_CITY = "rrel_city"


class WitTraitMessageClassesIdentifiers(Enum):
    pass


class WitIntentMessageClasses(Enum):
    UNKNOWN_CLASS = "concept_message_no_class"
