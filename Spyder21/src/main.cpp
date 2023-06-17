
#include <Arduino.h>
#include <SoftwareSerial.h>
#include "timers.h"
#include "input.h"
#include "gait.h"
#include "i2c.h"

// Soft Serial
SoftwareSerial softSerial(8,9);


void setup() 
{
  softSerial.begin(115200);
  actorsInit();
  tempInit();
  i2cInit();
  servoInit();
  timersInit();
  inputInit();
}


void loop() 
{
  inputHandle();
  timersTick();
  gait();
}
