#!/usr/bin/env python
#encoding=utf-8

import time

format_time = {
    19: '%Y-%m-%d %H:%M:%S',
    8: '%Y%m%d',
    6: '%Y%m',
    10: '%Y-%m-%d',
    16: '%Y-%m-%d %H:%M',
    17: '%Y%m%d-%H:%M:%S'
}

# Get demand time from all kinds of original time format after delay without specified type
# Args: [original_time] [delay] [output_fmt:{0,6,8,10,16,17,19}]
# Input format(Any one of them): 
#   201809
#   20180910
#   2018-09-10
#   2018-09-10 18:00
#   20180910-18:00:00
#   2018-09-10 18:00:00
#   1536573600(int)
#   1536573600.00(float)
# Return format(Any one of them): 
#   201809
#   20180910
#   2018-09-10
#   2018-09-10 18:00
#   20180910-18:00:00
#   2018-09-10 18:00:00
#   1536573600(int)
def get_time(ts=None, delay=0, fmt=19):
    try:
        # Get timestamp
        if not ts:
            ts = time.time()
        elif isinstance(ts, time.struct_time):
            ts = time.mktime(ts)
        elif isinstance(ts, str) or isinstance(ts, unicode):
            ts = time.mktime(time.strptime(ts, format_time[len(ts)]))
        # Calculate
        ts = int(ts) + delay
        # Output
        if fmt in format_time:
            return time.strftime(format_time[fmt], time.localtime(ts))
        else:
            return ts
    except:
        return None

# Main
if __name__ == '__main__':
    get_time()