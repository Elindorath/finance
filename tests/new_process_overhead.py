#! /usr/bin/env python

from multiprocessing import Pool

from perf_context import timed_performance


def noop():
    pass

with timed_performance():
    process = Process(target=noop)

    process.start()

    process.join()
