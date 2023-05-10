#include "sensors.h"

#define U_PIN A2
#define I_PIN A3

OneWire oneWire(10);
DallasTemperature sensors(&oneWire);
DeviceAddress temp1, temp0;

float t0 = 0, t1 = 0, vol = 0, cur = 0, mah = 0;
int sens[20][5];


void tempInit()
{
  sensors.begin();
  sensors.getAddress(temp0, 0);
  sensors.getAddress(temp1, 1);
  gettemp();
}

void gettemp() 
{
  sensors.requestTemperatures();
  t0 = sensors.getTempC(temp0);
  t1 = sensors.getTempC(temp1);
}

void getsens() 
{
  int i, j;
  float in[2], sum[2];

  in[0] = analogRead(U_PIN);
  in[1] = analogRead(I_PIN);

  for (i = 0; i < 2; i++)
    sum[i] = 0;

  for (i = 0; i < 20; i++)
  {
    if (i == 19)
      for (j = 0; j < 2; j++)
      {
        sens[i][j] = in[j];
        sum[j] = sum[j] + in[j];
      }
    else
      for (j = 0; j < 2; j++)
      {
        sens[i][j] = sens[i + 1][j];
        sum[j] = sum[j] + sens[i][j];
      }
  }

  vol = sum[0] / 20.0 * 0.0151;
  cur = (512.0 - (sum[1] / 20.0)) * 0.0264865;
  mah = mah + vol * cur / 72000.0;
}

void sendSensors(SoftwareSerial ser)
{
  ser.println("<V=" + String(vol) + ">");
  ser.println("<I=" + String(cur) + ">");
  ser.println("<T1=" + String(t0) + ">");
  ser.println("<T2=" + String(t1) + ">");
  ser.println("<W=" + String(mah) + ">");
}