import feedparser
import json
import redis
import time
from datetime import datetime

channel_name = 'scoreboard'

#can probably be extended to a generic rss provider
def main():
    r = redis.Redis()
    while True:
        feed = feedparser.parse('http://rss.cbc.ca/lineup/world.xml')
        msgs = ['CBC Headlines:']
        entries = feed['entries']
        entries.sort(reverse=True,key=lambda entry: datetime.strptime(entry.published,"%a, %d %b %Y %H:%M:%S %Z"))
        msgs.append('World:')
        for entry in entries[0:10]:
            msgs.append(entry.title)
        feed = feedparser.parse('http://rss.cbc.ca/lineup/canada.xml')
        entries = feed['entries']
        entries.sort(reverse=True,key=lambda entry: datetime.strptime(entry.published,"%a, %d %b %Y %H:%M:%S %Z"))
        msgs.append('Canada:')
        for entry in entries[0:10]:
            msgs.append(entry.title)
        data_for_board = json.dumps({'provider':'cbc','messages':msgs,'append':False})
        r.publish(channel_name,data_for_board)
        time.sleep(1*60*60) #update every 1 hour
     



if __name__ == '__main__':
    main()