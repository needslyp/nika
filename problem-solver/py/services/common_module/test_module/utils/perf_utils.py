"""
Copyright (c) 2021 Intelligent Semantic Systems LLC, All rights reserved.
Author Alexandr Zagorskiy
"""

import cProfile
import pstats
from functools import wraps
from pathlib import Path
from time import time

from common.sc_log import Log
from common_module.constant.extension import StatExtension


def timing(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        time_start = time()
        result = func(*args, **kwargs)
        exec_time = time() - time_start
        Log(timing.__name__).info(f"args:[{args}, {kwargs}] took: {exec_time} sec")
        return result

    return wrap


def profileit(profile_fname, sort_field="cumtime"):
    """
    Parameters
    ----------
    profile_fname
        profile output file name
    sort_field
        "calls"     : (((1,-1),              ), "call count"),
        "ncalls"    : (((1,-1),              ), "call count"),
        "cumtime"   : (((3,-1),              ), "cumulative time"),
        "cumulative": (((3,-1),              ), "cumulative time"),
        "file"      : (((4, 1),              ), "file name"),
        "filename"  : (((4, 1),              ), "file name"),
        "line"      : (((5, 1),              ), "line number"),
        "module"    : (((4, 1),              ), "file name"),
        "name"      : (((6, 1),              ), "function name"),
        "nfl"       : (((6, 1),(4, 1),(5, 1),), "name/file/line"),
        "pcalls"    : (((0,-1),              ), "primitive call count"),
        "stdname"   : (((7, 1),              ), "standard name"),
        "time"      : (((2,-1),              ), "internal time"),
        "tottime"   : (((2,-1),              ), "internal time"),
    Returns
    -------
    None
    """

    def print_profiler(profile_input_file, profile_output_file, sort_field="cumtime"):
        write_param = "a" if profile_input_file.exists() else "w"
        with open(profile_output_file, write_param) as f:
            stats = pstats.Stats(str(profile_input_file), stream=f)
            stats.strip_dirs().sort_stats(sort_field)
            stats.print_stats()

    def get_profile_path(profile_file):
        base_path = Path(__file__).parent.absolute() / StatExtension.STAT.value
        base_path.mkdir(parents=True, exist_ok=True)
        return base_path / profile_file

    def actual_profileit(func):
        def wrapper(*args, **kwargs):
            profile_path = get_profile_path(profile_fname)
            stat_path = f"{profile_path}.{StatExtension.STAT.value}"
            profiler = cProfile.Profile()
            result = profiler.runcall(func, *args, **kwargs)
            profiler.dump_stats(profile_path)
            print_profiler(profile_path, stat_path, sort_field)
            Log(profileit.__name__).info(f"dump stat in {stat_path}")
            return result

        return wrapper

    return actual_profileit
