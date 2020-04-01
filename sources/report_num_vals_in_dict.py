import os

def report_freqs(frequencies, key=None, reverse=False, number=None, width=None):
    total = sum(frequencies.values())
    maxratio = max(frequencies.values()) / total
    
    maxval_w = max(map(len, map(str, frequencies.values())))
    maxkey_w = max(map(len, map(str, frequencies.keys())))

    if os.isatty(1):
        columns, rows = os.get_terminal_size()
    else:
        columns, rows = 80, 24

    if number is None:
        number = len(frequencies)
    if width:
        columns = width

    barspace = columns - maxkey_w - maxval_w - 13

    for i, k in enumerate(sorted(frequencies, key=key, reverse=reverse)):
        if i >= number:
            break
        ratio = frequencies[k] / total
        bar_w = round(ratio / maxratio * barspace)
        print('{who:{w1}}: {freq:{w2}} ({perc:5.2f}%) {bar}'.format(who=k, freq=frequencies[k], perc=100 * ratio,
                                                                    bar=bar_w * '\u25a0', w1=maxkey_w, w2=maxval_w))

