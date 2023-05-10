#include <Arduino.h>
#include <SoftwareSerial.h>
#include "actors.h"
#include "servo.h"
#include "sensors.h"
#include "i2c.h"

// Timers
unsigned long senstimer;
unsigned long sendtimer;
unsigned long temptimer;

// I2C 
int adr = 0;
int cmd = 0;

// State
int led = 0;
int rgb = 0;
int fan = 0;
int mode;
int state = 0;

// Soft Serial
SoftwareSerial softSerial(8,9);


void setup() 
{
  senstimer = millis();
  sendtimer = millis();

  softSerial.begin(115200);

  tempInit();
  i2cInit();
  servoInit();
  actorsInit();

  bitSet(mode, 4);
}


void loop() 
{
  if (sendtimer + 1000 < millis())
  {
    sendSensors(softSerial);
    sendtimer = millis();
  }

  if (senstimer + 50 < millis())
  {
    getsens();
    senstimer = millis();
  }

  if (temptimer + 10000 < millis())
  {
    gettemp();
    temptimer = millis();
  }

  if(adr == 1 and cmd != 0)
  {
    if (cmd == 13)  // workaround for transmition error causing cmd==0
      cmd = 0;

    if (cmd < 5)
      mode = 1 << cmd;

    if (cmd == 8)
    {
      if (led == 0)
      {
        ledON();
        led = 1;
      }
      else
      {
        ledOFF();
        led = 0;
      }
    }

    if (cmd == 10)
    {
      if (fan == 0)
      {
        fanON();
        fan = 1;
      }
      else
      {
        fanOFF();
        fan = 0;
      }
    }

    if (cmd == 9)
    {
      if (rgb == 0)
      {
        rgbON();
        rgb = 1;
      }
      else
      {
        rgbOFF();
        rgb = 0;
      }
    }
  }
  adr = 0;
  cmd = 0;

  state = (fan<<7) + (rgb<<6) + (led<<5) + mode;
}
