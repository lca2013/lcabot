#!/usr/bin/python2.4

# rt -- let people know about new tickets in RT

import datetime
import rtlib
import shelve

class RtHelper(object):
    def __init__(self, log, conf):
        self.log = log
        self.conf = conf

        self.data = shelve.open('commands/rt.slf', writeback=True)
        self.data.setdefault('tickets', {})

    # Things you're expected to implement
    def Name(self):
        """Who am I?"""
        return 'rthelper'

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

        s = rtlib.Rt('%s/REST/1.0' % self.conf['rt']['url'],
                     self.conf['rt']['user'],
                     self.conf['rt']['password'])
        if not s.login():
            yield (None, 'msg', ('RT login for %s failed'
                                 % self.conf['rt']['user']))
        self.log('[Logged into RT]')

        for queue in self.conf['rt']['queues']:
            self.log('[Checking RT queue %s]' % queue)
            self.data['tickets'].setdefault(queue, {})
            for ticket in s.search(Queue=queue, Status='open'):
                tid = ticket['id']
                short_tid = tid.split('/')[1]
                url = ('%s/Ticket/Display.html?id=%s'
                       %(self.conf['rt']['url'], short_tid))

                if not tid in self.data['tickets'][queue]:
                    yield (None, 'msg',
                           ('[rt] new %s in %s: %s ( %s )'
                            %(tid, ticket['Queue'], ticket['Subject'], url)))
                    self.data['tickets'][queue][tid] = datetime.datetime.now()

                else:
                    delay = (datetime.datetime.now() -
                             self.data['tickets'][queue][tid])
                    if delay.days > 0:
                        yield (None, 'msg',
                               ('[rt] reminder for %s in %s: %s ( %s )'
                                %(tid, ticket['Queue'], ticket['Subject'],
                                  url)))
                        self.data['tickets'][queue][tid] = \
                            datetime.datetime.now()

    def Cleanup(self):
        """We're about to be torn down."""
        self.data.close()


def Init(log, conf):
    """Initialize all command classes."""
    yield RtHelper(log, conf)
