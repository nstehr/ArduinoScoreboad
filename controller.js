var SerialPort = require("serialport").SerialPort
var redis = require("redis")
var _ = require("underscore")

var subscriber = redis.createClient();
var serialPort = new SerialPort("/dev/tty.usbmodemfd121",{
   baudrate:9600
});

var CHANNEL_NAME = "scoreboard";
var messageQueue = [];
var messageIndex = 0;

//serial port setup
serialPort.on("open",function(){
    console.log("connection to ardunio established");
    //handler for getting data from arduino
    serialPort.on('data',onDataReceived);	
    //prime the device with an initial string
    writeToScoreboard("Nathan's Super Scoreboard");
});
//handle messages from publishers
//interested in writing to the board
subscriber.on("message",onNewMsgForScoreboard);
subscriber.subscribe(CHANNEL_NAME)

function onDataReceived(data){
	//leverage the fact that we only get the data
	//when the board is ready for a potentially new
	//string, so we don't need to decode the data
	if(messageQueue.length > 0){
				var message = messageQueue[messageIndex];
				console.log(message.message);
				writeToScoreboard(message.message);
				messageIndex++;
				if(messageIndex >= messageQueue.length)
				    messageIndex = 0;
			}
	
}

function writeToScoreboard(text){
	serialPort.write(text+"\n",function(err,result){
	if(err)
	   console.log(err);
});
}

//the json message should be in the format:
//{'provider':'test','messages':['a','b','c'],'append':false}
//where provider is a string indicating the 
//datasource and append is whether or not to append or
//replace the messages from the same provider
function onNewMsgForScoreboard(channel,jsonMessage){
	var data = JSON.parse(jsonMessage);
	if(data.append == false){
		messageQueue = _.reject(messageQueue,function(msg){return msg.provider == data.provider});
	}
	
	for (var i=0;i<data.messages.length;i++){
		var message = {}
		message.message = data.messages[i];
		message.provider = data.provider;
	    messageQueue.push(message);
	}
}