"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from threading import RLock

from common import ScKeynodes
from common_module.constant.identifiers import IdentifiersEnums
from common_module.keynode.meta_keynodes import MetaGlobalScKeynodes
from sc import ScAddr, ScMemoryContext


class GlobalScKeynodes(ScKeynodes, metaclass=MetaGlobalScKeynodes):
    lock = RLock()

    def __init__(self, context: ScMemoryContext):
        with self.lock:
            super().__init__(context)
            identifiers = []
            for enum_class in IdentifiersEnums:
                identifiers += [identifier.value for identifier in enum_class]
            self.add_keynodes(identifiers)

    def __getitem__(self, sys_idtf: str) -> ScAddr:
        with self.lock:
            return super().__getitem__(sys_idtf)

    def add_keynodes(self, identifiers):
        with self.lock:
            for identifier in identifiers:
                if identifier != "":
                    self.__getitem__(identifier)
