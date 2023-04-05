#include <Arduino.h>

// I2C
#include <Wire.h>
int adr=0;
int rcv[10];
int bt=0;

// Soft Serial
#include <SoftwareSerial.h>
SoftwareSerial softSerial(8,9);

#define U_PIN A2
#define I_PIN A3
#define LED_PIN 6
#define FAN_PIN 3

unsigned long senstimer;
unsigned long sendtimer;
unsigned long temptimer;

// Temperature
#include <OneWire.h>
#include <DallasTemperature.h>
OneWire oneWire(10);
DallasTemperature sensors(&oneWire);
DeviceAddress temp1, temp0;
float t0 = 0, t1 = 0, vol = 0, cur = 0, mah = 0;
int sens[20][5];

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


void recvData(int bts)
{
  bt=bts;
  for(int i=0; i<bts; i++)
    rcv[i]=Wire.read();
  adr = rcv[0];
}

void sendData()
{

  Wire.write(123);

}


void setup() {
  
  pinMode(LED_PIN, OUTPUT);
  analogWrite(LED_PIN, 0);

  senstimer = millis();
  sendtimer = millis();

  // Soft Serial
  softSerial.begin(115200);

  // Temperature
  sensors.begin();
  sensors.getAddress(temp0, 0);
  sensors.getAddress(temp1, 1);
  gettemp();

  // I2C
  Wire.begin(0x11);
  Wire.onRequest(sendData);
  Wire.onReceive(recvData);

}

void loop() {
  
  if (sendtimer + 1000 < millis())
  {
    softSerial.println("<V=" + String(vol) + ">");
    softSerial.println("<I=" + String(cur) + ">");
    softSerial.println("<T1=" + String(t0) + ">");
    softSerial.println("<T2=" + String(t1) + ">");
    softSerial.println("<W=" + String(mah) + ">");
    sendtimer = millis();
  }

  if (adr==10)
  {
    analogWrite(LED_PIN, 255);
    adr=0;
  }
  if (adr==11)
  {
    analogWrite(LED_PIN, 0);
    adr=0;
  }

  if (adr==12)
  {
    analogWrite(FAN_PIN, 255);
    adr=0;
  }
  if (adr==13)
  {
    analogWrite(FAN_PIN, 0);
    adr=0;
  }


   
  if(bt>0)
  {
    softSerial.print("I2C >> ");
    for(int i=0; i<bt; i++)
    {
      softSerial.print(rcv[i]);
      softSerial.print(" ");
      rcv[i]=0;
    }
    softSerial.println();
    bt=0;
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

}

