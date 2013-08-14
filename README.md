Arduino Scoreboard
=============

One day at the day job, the meme of 'keeping score' evolved after one of our daily scrums.  
I took this past funny jokes and whiteboards and with this project created an actual scrolling marquee/scoreboard :)

The hardware involved is an arduino uno, and currently 2 Sure Electronics 3208 LED Matrix displays.  

In attempt to keep the arduino code as simple as possible the arduino will just listen for new
strings to display on the serial port, and will notify (also via the serial port) when it
is in a good state for accepting a new string as to not write anything before the last message
has scrolled of the marquee.  A node.js script is responsible for managing the queue of messages
to display on the marquee.

## API
To display messages on the board, I have created a simple API using Redis pub/sub.
The node.js script subscribes to a channel, and any redis client can publish messages
to it.  To get your message displayed on the marquee, publish a JSON message in the following 
format:

```javascript
{'provider':'test','messages':['a','b','c'],'append':false}
```

Where provider is the unique name of the datasource, messages is a list
of message you wish to have displayed, and append is whether or not
you want to append to the queue or replace messages in the queue. Only messages
with the same provider will be replaced.

See /publishers for some example publishing clients

## Author

Nathan Stehr

