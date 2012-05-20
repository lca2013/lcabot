#!/usr/bin/python2.4

# countdown -- provide a count down to important LCA deadlines

import datetime

import utility

class CountDown(object):
    def __init__(self, log, conf):
        self.log = log
        self.conf = conf
        self.last_topic = datetime.datetime(1970,1,1)

    # Things you're expected to implement
    def Name(self):
        """Who am I?"""
        return 'countdown'

    def Verbs(self):
        """Return the verbs which this module supports

        Takes no arguments, and returns an array of strings.
        """

        return ['countdown', 'settopic']

    def Help(self, verb):
        """Display help for a verb

        Takes the name of a verb, and returns a string which is the help
        message for that verb.
        """

        if verb == 'countdown':
            return 'count down the number of days to important events'
        elif verb == 'settopic':
            return 'set the channel topic to a motivational countdown'
        return ''

    def Command(self, channel, verb, line):
        """Execute a given verb with these arguments
        
        Takes the verb which the user entered, and the remainder of the line.
        Returns a string which is sent to the user.
        """

        if verb == 'countdown':
            for event, days in self._get_days():
                yield (channel, 'msg', 'Days until %s: %d' %(event, days))

        elif verb == 'settopic':
            yield(channel, 'topic', self._make_topic())

        else:
            yield

    def NoticeUser(self, channel, user):
        """We just noticed this user. Either they joined, or we did."""
        yield

    def HeartBeat(self):
        """Gets called at regular intervals"""

        # Check if its time for the daily topic update
        now = datetime.datetime.now()
        if now.day != self.last_topic.day:
            yield (None, 'topic', self._make_topic())

    def Cleanup(self):
        """We're about to be torn down."""
        pass

    # Your own internal helpers
    def _get_days(self):
        for e in self.conf['countdown']:
            event = e['name']
            dt = utility.ParseDateTime(e['datetime'])

            delta = dt - datetime.datetime.now()
            if delta.days > 0:
                yield(event, delta.days)

    def _make_topic(self):
        now = datetime.datetime.now()
        topic = []
        for event, days in self._get_days():
            topic.append('%d days until %s' %(days, event))
        self.last_topic = now            
        return '; '.join(topic)


def Init(log, conf):
    """Initialize all command classes."""
    yield CountDown(log, conf)
