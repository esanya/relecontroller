# Archwomen.ics file

```
BEGIN:VCALENDAR
PRODID:-//Mozilla.org/NONSGML Mozilla Calendar V1.1//EN
VERSION:2.0
BEGIN:VEVENT
CREATED:20170220T182458Z
LAST-MODIFIED:20170220T182458Z
DTSTAMP:20170220T182458Z
UID:a79d1ffd-f62b-4c14-98b7-22eaa494a7fd
SUMMARY:Arch Linux Women Monthly Project Meeting
RRULE:FREQ=MONTHLY;BYDAY=2SA
DTSTART;VALUE=DATE:20170211T160000Z
DTEND;VALUE=DATE:20170211T180000Z
LOCATION:#archlinux-women @ irc.freenode.net
DESCRIPTION:https://archwomen.org/wiki/meetings
URL:https://archwomen.org/wiki/meetings:start
TRANSP:TRANSPARENT
END:VEVENT
BEGIN:VEVENT
CREATED:20120514T060851Z
LAST-MODIFIED:20120514T061031Z
DTSTAMP:20120514T061031Z
UID:e0639f9c-5ab0-4001-9da9-3003611b6e94
SUMMARY:Bug Day
RRULE:FREQ=WEEKLY
DTSTART;VALUE=DATE:20120821T000000Z
DTEND;VALUE=DATE:20120822T000000Z
LOCATION:#archlinux-bugs @ Freenode IRC
DESCRIPTION:http://bugs.archlinux.org/
TRANSP:TRANSPARENT
END:VEVENT
BEGIN:VEVENT
CREATED:20170220T182458Z
LAST-MODIFIED:20170220T182458Z
DTSTAMP:20170220T182458Z
UID:0c9acbbb-f82e-444d-b941-50c3a9953d86
SUMMARY:Test unique date
DTSTART;VALUE=DATE:20170303T110000Z
DTEND;VALUE=DATE:20170303T113000Z
LOCATION:My computer
DESCRIPTION:A test for a one time event
TRANSP:OPAQUE
END:VEVENT
END:VCALENDAR`
```

# Python code

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Parse ical file and report all events in the next 2 months """

from datetime import datetime, timedelta, timezone
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

icalfile = open('Archwomen.ics', 'rb')
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
```

# Output

```
03/11/17 16:00 UTC  Arch Linux Women Monthly Project Meeting: https://archwomen.org/wiki/meetings - #archlinux-women @irc.freenode.net

04/08/17 16:00 UTC  Arch Linux Women Monthly Project Meeting: https://archwomen.org/wiki/meetings - #archlinux-women @irc.freenode.net

02/28/17 00:00 UTC  Bug Day: http://bugs.archlinux.org/ - #archlinux-bugs @ Freenode IRC

03/07/17 00:00 UTC  Bug Day: http://bugs.archlinux.org/ - #archlinux-bugs @ Freenode IRC

03/14/17 00:00 UTC  Bug Day: http://bugs.archlinux.org/ - #archlinux-bugs @ Freenode IRC

03/21/17 00:00 UTC  Bug Day: http://bugs.archlinux.org/ - #archlinux-bugs @ Freenode IRC

03/28/17 00:00 UTC  Bug Day: http://bugs.archlinux.org/ - #archlinux-bugs @ Freenode IRC

04/04/17 00:00 UTC  Bug Day: http://bugs.archlinux.org/ - #archlinux-bugs @ Freenode IRC

04/11/17 00:00 UTC  Bug Day: http://bugs.archlinux.org/ - #archlinux-bugs @ Freenode IRC

04/18/17 00:00 UTC  Bug Day: http://bugs.archlinux.org/ - #archlinux-bugs @ Freenode IRC

03/03/17 11:00 UTC-03/03/17 11:30 UTC Test unique date: A test for a one time event - My computer
```

# Todo

* order dates soonist to now to farthest
* some sort of error handling?