#include "i2c.h"

int adr = 0;
int cmd = 0;
int state = 0;

void recvData(int bts)
{
  int rcv[10];
  for(int i = 0; i < bts; i++)
    rcv[i] = Wire.read();
  adr = rcv[0];
  if(bts == 1)
    cmd = 255;
  else
    cmd = rcv[1];
}

void sendData()
{
  Wire.write(state & 255);
}

void i2cInit()
{
  Wire.begin(0x11);
  Wire.onRequest(sendData);
  Wire.onReceive(recvData);
}