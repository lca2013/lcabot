#!/usr/bin/python

import datetime
import json
import time
import urllib


URL = 'http://lca2012.linux.org.au/programme/schedule/json'

remote = urllib.urlopen(URL)
data = json.loads(remote.read())

for ent in data:
  start = datetime.datetime(*(time.strptime(ent['Start'],
                                            '%Y-%m-%d %H:%M:00')[0:5]))

  print '----------------------'
  print ent
  print
  print ent['Title']
  print start
  print ent['Room Name']
  print '%s#%s' %(URL, ent['Id'])

  print
