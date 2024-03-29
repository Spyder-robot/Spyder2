#include "servo.h"

char serdir[] = {1,1,1,1,1,1,1,1,1,1,-1,-1,1,-1,-1,1,-1,-1};
float sermin[] = {-PI/3,0,0};
float sermax[] = {PI/3,PI/2,PI/2};
int serzero[] = {512,512,512};
float koeff = 1.0/PI*180.0/300.0*1024.0;


void servoTurn(int ID, float ang, int spd)
{
  int ticks;
  int joint;

  joint = (ID - 1) % 3;
  ang = constrain(ang, sermin[joint], sermax[joint]);
  ticks = serzero[joint] + serdir[ID - 1] * int(ang * koeff);
  Dynamixel.moveSpeed(ID, ticks, spd);
}


void waitWhileMoving()
{
  bool mov = true;
  while(mov)
  {
    mov = false;
    for(int i = 1; i <= 18; i++)
      if(Dynamixel.moving(i) == 1)
        mov = true;
  }
}


void initMove()
{
  int i;

  for(i = 0; i < 6; i++)
  {
    servoTurn(i * 3 + 1, 0, 100);
    servoTurn(i * 3 + 2, PI / 2, 100);
    servoTurn(i * 3 + 3, PI / 4, 100);
  }

  waitWhileMoving();

  for (i = 0; i < 6; i++)
    servoTurn(i * 3 + 3, 0, 100);

  waitWhileMoving();

  for (i = 0; i < 6; i++)
    servoTurn(i * 3 + 3, PI / 4, 100);

  waitWhileMoving();
}


void servoInit()
{
  Dynamixel.setSerial(&Serial);
  Dynamixel.begin(1000000, 2);
  initMove();
}


void curPosition(float *srvs)
{
  int joint;
  for(int i = 1; i <= 18; i++)
  {
    joint = (i - 1) % 3;
    srvs[i-1] = (float(Dynamixel.readPosition(i)) - serzero[joint]) / (serdir[i - 1] * koeff);
  }
}