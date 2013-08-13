import urllib2
import json
import redis
import time

channel_name = 'scoreboard'

def main():
    r = redis.Redis()
    while True:
        response = urllib2.urlopen('http://api.openweathermap.org/data/2.5/find?q=Ottawa,ca&units=metric&mode=json')
        data = json.load(response)
        info = data['list'][0]
        weather_info = info['weather'][0]['description']
        current_temp = info['main']['temp']
        data_for_board = json.dumps({'provider':'weather','messages':['Weather for Ottawa,ON:',str(current_temp)+'C',weather_info],'append':False})
        r.publish(channel_name,data_for_board)

        time.sleep(15*60) #update every 15 minutes
     



if __name__ == '__main__':
    main()