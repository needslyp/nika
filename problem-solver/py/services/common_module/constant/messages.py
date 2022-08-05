"""
    Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
    Author Nikiforov Sergei
"""

from enum import Enum


class CustomExceptionMessages(Enum):
    MESSAGE_TYPE_UNDEFINED = "Message type is undefined"
    TEXT_LINK_NOT_FOUND = "Text link is not found"


class MessageTexts(Enum):
    EMPTY_MESSAGE_TEXT = "..."
