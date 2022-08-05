"""
    Copyright (c) 2020 Intelligent Semantic Systems LLC, All rights reserved.
    Author Ruslan Korshunov
"""

from threading import RLock


class MetaGlobalScKeynodes(type):
    lock = RLock()
    instance = None

    def __call__(cls, *args, **kwargs):
        with cls.lock:
            if cls.instance is None:
                cls.instance = super().__call__(*args, **kwargs)
        return cls.instance
