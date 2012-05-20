#!/usr/bin/python2.4

# reminder -- remind channels about events

import datetime
import shelve

import utility

class Reminder(object):
    def __init__(self, log, conf):
        self.log = log
        self.conf = conf

        self.data = shelve.open('commands/reminder.slf', writeback=True)
        self.data.setdefault('reminders', {})

        self.sorted_times = self.data['reminders'].keys()
        self.sorted_times.sort()

    # Things you're expected to implement
    def Name(self):
        """Who am I?"""
        return 'reminder'

    def Verbs(self):
        """Return the verbs which this module supports

        Takes no arguments, and returns an array of strings.
        """

        return ['agenda', 'setreminder']

    def Help(self, verb):
        """Display help for a verb

        Takes the name of a verb, and returns a string which is the help
        message for that verb.
        """

        if verb == 'setreminder':
            return 'set a reminder for later -- time format is YYYYMMDD HHMM'
        elif verb == 'agenda':
            return 'show the agenda for today (only future events shown)'
        return ''

    def Command(self, channel, verb, line):
        """Execute a given verb with these arguments
        
        Takes the verb which the user entered, and the remainder of the line.
        Returns a string which is sent to the user.
        """

        if verb == 'setreminder':
            elems = line.split(' ')
            dt = utility.ParseDateTime(' '.join(elems[0:2]))
            event = ' '.join(elems[2:])

            self.data['reminders'].setdefault(dt, [])
            self.data['reminders'][dt].append(event)
            self.sorted_times = self.data['reminders'].keys()
            self.sorted_times.sort()

            yield (channel, 'msg', 'Created "%s" for %s' %(event, dt))

        elif verb == 'agenda':
            if len(self.sorted_times) == 0:
                yield (channel, 'msg', 'There are no events')

            else:
                one_day = datetime.datetime.now() + datetime.timedelta(days=1)
                idx = 0
                while (idx < len(self.sorted_times) and
                       idx < 20 and
                       self.sorted_times[idx] < one_day):
                    dt = self.sorted_times[idx]
                    events = '; '.join(self.data['reminders'][dt])
                    yield (channel, 'msg', '%s: %s' %(dt, events))
                    idx += 1

                if idx == 20:
                    yield (channel, 'msg', '[snip]')

        else:
            yield

    def NoticeUser(self, channel, user):
        """We just noticed this user. Either they joined, or we did."""
        yield

    def HeartBeat(self):
        """Gets called at regular intervals"""

        five_minutes = datetime.datetime.now() + datetime.timedelta(seconds=300)
        idx = 0
        while (idx < len(self.sorted_times) and
               idx < 1 and
               self.sorted_times[idx] < five_minutes):
            dt = self.sorted_times[idx]
            for event in self.data['reminders'][dt]:
                yield (None, 'msg',
                       '[reminder] %s starts at %s' %(event, dt))
            del self.data['reminders'][dt]

            idx += 1

        self.sorted_times = self.data['reminders'].keys()
        self.sorted_times.sort()

    def Cleanup(self):
        """We're about to be torn down."""
        self.data.close()


def Init(log, conf):
    """Initialize all command classes."""
    yield Reminder(log, conf)
