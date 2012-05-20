#!/usr/bin/python2.4

# simple IRC operations

import datetime


OPS = ['evil_steve', 'mikal']


class IRCHelper(object):
    def __init__(self, log, conf):
        self.log = log
        self.conf = conf

    # Things you're expected to implement
    def Name(self):
        """Who am I?"""
        return 'irchelper'

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

        if user in OPS:
            yield('chanserv', 'msg', 'op %s %s' %(channel, user))

    def HeartBeat(self):
        """Gets called at regular intervals"""
        yield

    def Cleanup(self):
        """We're about to be torn down."""
        pass


def Init(log, conf):
    """Initialize all command classes."""
    yield IRCHelper(log, conf)
