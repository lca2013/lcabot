#!/usr/bin/python

import datetime
import time

def ParseDateTime(s):
    """Turn a string into a datetime. Format is YYYYMMDD HHMM."""
    return datetime.datetime(*time.strptime(s, "%Y%m%d %H%M")[0:5])
