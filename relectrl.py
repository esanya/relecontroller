import sys
import urllib2
import icalendar

url = sys.argv[1]

response = urllib2.urlopen(url)
webContent = response.read()

#print(webContent[0:300])

dt = icalendar.Calendar.from_ical(webContent)

#print(dt)

for component in dt.walk():
    print component.name

    if component.name == "VEVENT":
        print(component.get('summary'))
        print(component.get('dtstart'))
        print(component.get('dtend'))
        print(component.get('dtstamp'))



