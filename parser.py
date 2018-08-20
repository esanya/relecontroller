
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Parse ical file and report all events in the next 2 months """

from datetime import datetime, timedelta, timezone
import sys
import icalendar
from dateutil.rrule import *


def parse_recurrences(recur_rule, start, exclusions):
    """ Find all reoccuring events """
    rules = rruleset()
    first_rule = rrulestr(recur_rule, dtstart=start)
    rules.rrule(first_rule)
    if not isinstance(exclusions, list):
        exclusions = [exclusions]
        for xdate in exclusions:
            try:
                rules.exdate(xdate.dts[0].dt)
            except AttributeError:
                pass
    now = datetime.now(timezone.utc)
    this_year = now + timedelta(days=60)
    dates = []
    for rule in rules.between(now, this_year):
        dates.append(rule.strftime("%D %H:%M UTC "))
    return dates

if ( len(sys.argv) > 1 ):
    icalfile = open(sys.argv[1], 'rb')
else:
    icalfile = sys.stdin

gcal = icalendar.Calendar.from_ical(icalfile.read())
for component in gcal.walk():
    if component.name == "VEVENT":
        summary = component.get('summary')
        description = component.get('description')
        location = component.get('location')
        startdt = component.get('dtstart').dt
        enddt = component.get('dtend').dt
        exdate = component.get('exdate')
        if component.get('rrule'):
            reoccur = component.get('rrule').to_ical().decode('utf-8')
            for item in parse_recurrences(reoccur, startdt, exdate):
                print("{0} {1}: {2} - {3}\n".format(item, summary, description, location))
        else:
            print("{0}-{1} {2}: {3} - {4}\n".format(startdt.strftime("%D %H:%M UTC"), enddt.strftime("%D %H:%M UTC"), summary, description, location))
icalfile.close()
