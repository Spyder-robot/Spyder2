#ifndef SERVO
#define SERVO

#include <Arduino.h>
#include <DynamixelSerial.h>

void servoInit();

void servoTurn(int ID, float ang, int spd);

void waitWhileMoving();

void initMove();

#endif