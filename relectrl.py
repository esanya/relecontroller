import sys
import urllib2
import icalendar

if ( len(sys.argv) > 1 ):
    url = sys.argv[1]
    response = urllib2.urlopen(url)
    calendarText = response.read()
    #print(calendarText[0:300])
else:
    calendarText = sys.stdin.read()


dt = icalendar.Calendar.from_ical(calendarText)

#print(dt)

for component in dt.walk():
    print component.name

    if component.name == "VEVENT":
        print(component.get('summary'))
        print(component.get('dtstart'))
        print(component.get('dtend'))
        print(component.get('dtstamp'))



