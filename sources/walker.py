#!/usr/bin/env python3

import sys
import os
from os.path import isdir, join, getsize

topdir = os.environ['HOME']
if len(sys.argv) > 1:
    if isdir(sys.argv[1]):
        topdir = sys.argv[1]
    else:
        sys.exit('{}: {} is not a directory'.format(sys.argv[0], sys.argv[1]))

for thisdir, subdirs, nondirs in os.walk(topdir):
    total = 0

    for name in nondirs:
        path = join(thisdir, name)
        try:
            total += getsize(path)
        except OSError:
            pass

    if total:
        print('Files in {} use {} bytes'.format(thisdir, total))
