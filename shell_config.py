from importlib import reload
import datetime
import pprint

pp = pprint.pprint


def ft(timestamp, tz=None):
    if not tz:
        import tzlocal
        tz = tzlocal.get_localzone()
    elif isinstance(tz, str):
        import pytz
        tz = pytz.timezone(tz)
    return tz.localize(datetime.datetime.fromtimestamp(timestamp))


def l2l(long_lines):
    return [l for l in long_lines.split('\n') if l]


def clip(s):
    import pandas.io.clipboard
    pandas.io.clipboard.copy(s)


def commify(n):
    return f'{n:,d}'


def numformat(num, precision=2):
    num = int(num)
    if num == 0:
        return '0'
    import math
    log = math.floor(math.log(num, 1000))
    n = num // math.pow(1000, log)
    suffix = ['', 'K', 'M', 'B', 'T'][int(log)]
    return f'{n:.{precision}f}{suffix}'


def sizeformat(bytes, precision=2):
    bytes = int(bytes)
    if bytes == 0:
        return '0 Bytes'
    import math
    log = math.floor(math.log(bytes, 1024))
    n = bytes // math.pow(1024, log)
    suffix = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'][int(log)]
    return f'{n:.{precision}f}{suffix}'

