import urllib2
import json
import redis
import time
import datetime

channel_name = 'scoreboard'

def main():
    r = redis.Redis()
    while True:
        response = urllib2.urlopen('http://api.openweathermap.org/data/2.5/find?q=Ottawa,ca&units=metric&mode=json')
        data = json.load(response)
        info = data['list'][0]
        weather_info = info['weather'][0]['description']
        current_temp = info['main']['temp']
        messages = ['Weather for Ottawa,ON:','Currently:',str(current_temp)+'C',weather_info]
        #get the 5 day forecast
        response = urllib2.urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?q=Ottawa,ON&mode=json&units=metric&cnt=5')
        data = json.load(response)
        forecasts = data['list']
        messages.append('5 Day Forecast:')
        day = datetime.datetime.now()
        for forecast in forecasts:
            low = forecast['temp']['min']
            high = forecast['temp']['max']
            weather_info = forecast['weather'][0]['description']
            msg = "%s: Low: %0.2fC High: %0.2fC %s" % (day.strftime("%A, %B %d"),low,high,weather_info)
            messages.append(msg)
            day = day + datetime.timedelta(days=1)
        #prepare data for API call
        data_for_board = json.dumps({'provider':'weather','messages':messages,'append':False})
        r.publish(channel_name,data_for_board)

        time.sleep(15*60) #update every 15 minutes
     



if __name__ == '__main__':
    main()