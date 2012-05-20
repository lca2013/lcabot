#!/usr/bin/python2.4

# simple IRC operations

import datetime
import feedparser
import shelve
import unicodedata
import urllib2


# This should be in the config yaml
TWITTER_SEARCH = ('http://search.twitter.com/search.atom?q=%s&rpp=100'
                  '&result_type=mixed')

FEEDS = [TWITTER_SEARCH % 'lca2013',
         TWITTER_SEARCH % 'linux.conf.au',
         'http://identi.ca/search/notice/rss?q=lca2013']


def Normalize(value):
  normalized = unicodedata.normalize('NFKD', unicode(value))
  normalized = normalized.encode('ascii', 'replace')
  return normalized


class TwitterWatcher(object):
    def __init__(self, log, conf):
        self.log = log
        self.conf = conf

        self.data = shelve.open('commands/twitter.slf', writeback=True)
        self.data.setdefault('guids', {})

    # Things you're expected to implement
    def Name(self):
        """Who am I?"""
        return 'twitterwatcher'

    def Verbs(self):
        """Return the verbs which this module supports

        Takes no arguments, and returns an array of strings.
        """

        return []

    def Help(self, verb):
        """Display help for a verb

        Takes the name of a verb, and returns a string which is the help
        message for that verb.
        """
        return ''

    def Command(self, channel, verb, line):
        """Execute a given verb with these arguments
        
        Takes the verb which the user entered, and the remainder of the line.
        Returns a string which is sent to the user.
        """
        yield

    def NoticeUser(self, channel, user):
        """We just noticed this user. Either they joined, or we did."""
        yield

    def HeartBeat(self):
        """Gets called at regular intervals"""

        for feed in FEEDS:
            self.log('[Fetching %s]' % feed)
            remote = urllib2.urlopen(feed)
            lines = ''.join(remote.readlines())
            remote.close()
            d = feedparser.parse(lines)

            # Newest entries are first
            entries = d.entries
            entries.reverse()
            for ent in entries:
                tweet = Normalize(ent.title).replace('\r', '').replace('\n', ' ')
                self.log('Tweet found: %s' % tweet)
                if ent.guid not in self.data['guids']:
                    self.data['guids'][ent.guid] = True
                    yield(None, 'msg',
                          '[tweet] %s ( %s )' %(tweet, ent.link))

    def Cleanup(self):
        """We're about to be torn down."""
        self.data.close()


def Init(log, conf):
    """Initialize all command classes."""
    yield TwitterWatcher(log, conf)
