#include "timers.h"

#define CYCLE_TIME 50

extern SoftwareSerial softSerial;

unsigned long senstimer;
unsigned long sendtimer;
unsigned long temptimer;
unsigned long cycletimer;


void timersInit()
{
  senstimer = millis();
  sendtimer = millis();
  temptimer = millis();
  cycletimer = millis();
}


void timersTick()
{
  
  if(sendtimer + 1000 < millis())
  {
    sendSensors(softSerial);
    sendtimer = millis();
  }

  if(senstimer + 50 < millis())
  {
    getsens();
    senstimer = millis();
  }

  if(temptimer + 10000 < millis())
  {
    // gettemp();
    temptimer = millis();
  }

// leverage of cycle - to add

}