#ifndef SENSORS
#define SENSORS

#include <OneWire.h>
#include <DallasTemperature.h>
#include <SoftwareSerial.h>

void tempInit();

void gettemp();

void getsens();

void sendSensors(SoftwareSerial ser);

#endif
