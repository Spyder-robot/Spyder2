#include "actors.h"
#include <microLED.h>

microLED<16, 5, MLED_NO_CLOCK, LED_WS2818, ORDER_GRB, CLI_AVER, SAVE_MILLIS> strip;

// Constants
#define LED_PIN 6
#define FAN_PIN 3


void actorsInit()
{
  pinMode(LED_PIN, OUTPUT);
  analogWrite(LED_PIN, 0);

  strip.setBrightness(60);
  strip.clear();
  strip.show();
  delay(1);   
}


void ledON()
{
  analogWrite(LED_PIN, 255);
}


void ledOFF()
{
  analogWrite(LED_PIN, 0);
}


void fanON()
{
  analogWrite(FAN_PIN, 255);
}


void fanOFF()
{
    analogWrite(FAN_PIN, 0);
}


void rgbON()
{
  strip.fill(mGreen);
  strip.show();   
}


void rgbOFF()
{
  strip.clear();
  strip.show();
}