#include "input.h"

extern int adr;
extern int cmd;
extern int state;

extern SoftwareSerial softSerial;

int led = 0;
int rgb = 0;
int fan = 0;

int mode = 0;
int nextmode = 0;

int inpt = 0;

void inputInit()
{
  bitSet(mode, 4);
}


void inputHandle()
{
  if(adr == 1 and cmd != 0)
  {
    if(cmd == 13)  // workaround for transmition error causing cmd==0
      cmd = 0;

    if(cmd < 5)
      nextmode = 1<<cmd;

    if(cmd == 8)
    {
      if(led == 0)
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

    if(cmd == 10)
    {
      if(fan == 0)
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

    if(cmd == 9)
    {
      if(rgb == 0)
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
  
  if(adr == 2)
    inpt = cmd;

  adr = 0;
  cmd = 0;

  state = (fan<<7) + (rgb<<6) + (led<<5) + mode;
}