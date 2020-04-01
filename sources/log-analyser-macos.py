#!/usr/bin/env python3

import sys
import os
from report_num_vals_in_dict import report_nums

info = {}
lines = 0

with open('/var/log/system.log') as logfile:
    for line in logfile:
        parts = line.split()
        if len(parts) < 5:
            continue
        who = parts[4]
        pos = who.find('[')
        if pos != -1:
            who = who[:pos]
        count = info.setdefault(who, 0)
        info[who] = count + 1
        lines += 1

report_nums(info, sortkey=info.get, reverse=True)
