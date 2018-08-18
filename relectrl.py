import sys
import urllib2
import icalendar

url = sys.argv[1]

response = urllib2.urlopen(url)
webContent = response.read()

#print(webContent[0:300])

dt = icalendar.Calendar.from_ical(webContent)

print(dt)

