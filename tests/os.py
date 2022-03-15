#! /usr/bin/env python

import os


print(os.cpu_count())
print(len(os.sched_getaffinity(0)))
print(os.getloadavg())
