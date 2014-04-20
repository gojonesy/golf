# import library to do http requests
import urllib2

# import easy to use xml parser called minidom:
from xml.dom import minidom

#download the file:
xmldoc = minidom.parse(urllib2.urlopen('http://gd2.mlb.com/components/game/mlb/year_2014/batters/453400.xml'))

itemlist = xmldoc.getElementsByTagName('batting')
print len(itemlist)
print itemlist[0].attributes['s_hr'].value