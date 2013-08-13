#include <font_5x4.h>
#include <HT1632.h>
#include <images.h>

int i = 0;
int msgIndex = 0;
int insertIndex = 0;
int wd;

String msgStr = "";
const char * currentString;

const char* displayStrings[5];

#define DATA 2
#define WR 3
#define CS 4
#define CS2 5

#define BUFFER_SIZE 140

void setup () {
  Serial.begin(9600);
  HT1632.begin(CS, CS2, WR, DATA);
}

void loop () {
  
 while (Serial.available() > 0){
   char received = Serial.read();
   
   //definitely a better way to handle the input
   //but it works, revisit later...
   msgStr += received;
   if(received == '\n'){
    
      char charBuf[BUFFER_SIZE];
      msgStr.toCharArray(charBuf,BUFFER_SIZE);
      const char * buffer = charBuf;
      currentString = buffer;
      wd = HT1632.getTextWidth(currentString, FONT_5X4_WIDTH, FONT_5X4_HEIGHT);
      msgStr = ""; 
       
   }
   
 }
 
 
 if(i == 0)
     Serial.println("1");
 
  HT1632.drawTarget(BUFFER_BOARD(1));
  HT1632.clear();
  HT1632.drawText(currentString, 2*OUT_SIZE - i, 2, FONT_5X4, FONT_5X4_WIDTH, FONT_5X4_HEIGHT, FONT_5X4_STEP_GLYPH);
  HT1632.render();
  
  HT1632.drawTarget(BUFFER_BOARD(2));
  HT1632.clear();
  HT1632.drawText(currentString, OUT_SIZE - i, 2, FONT_5X4, FONT_5X4_WIDTH, FONT_5X4_HEIGHT, FONT_5X4_STEP_GLYPH);
  HT1632.render();
  
  
  i = (i+1)%(wd + OUT_SIZE * 2);
 
  delay(50);
}
