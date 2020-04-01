#!/usr/bin/env python3

import re
from report_num_vals_in_dict import report_freqs
from subprocess import Popen, PIPE
from collections import Counter


def get_log_freqs():
    counter = Counter()

    # Apr 13 14:46:23 adnovo.local kernel: BIOS-e820: [mem 0x0000000000000000- ....
    c_re = re.compile(r'\w{3} \d{2} \d{2}:\d{2}:\d{2} \S* (\S*): .*')

    with Popen(['journalctl'], stdout=PIPE, universal_newlines=True) as log:
        for line in log.stdout:
            match = c_re.search(line)
            if match:
                who = match.group(1)
                who = who.split('[')[0]
                counter[who] += 1
        log.stdout.close()
    return counter

if __name__ == '__main__':
    freqs = get_log_freqs()
    report_freqs(freqs, key=freqs.get, reverse=True)
