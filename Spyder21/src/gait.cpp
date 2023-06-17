#include "gait.h"

extern SoftwareSerial softSerial;
extern int mode, nextmode;
extern int inpt;

int gaitNo = 0;
int stage = 0;
bool readyToChangeMode = true;
bool readyToNextStage = true;

float xyzStart[18];
float xyzFinish[18];
float xyzCur[18];

int stageDuration = 500;
long startTime;


void IIK(float *xyz, float *ang)
{
  float AB = 53.05;
  float DE = 136.0;
  float BD = 62.27585407;
  float CBD = 0.229711485;
  float BD2 = 3878.282;
  float DE2 = 18496.00;

  float FE, JE, BE, JBE, EBD, BDE;

  FE = sqrt(xyz[0] * xyz[0] + xyz[1] * xyz[1]);
  JE = FE - AB;
  BE = sqrt(xyz[2] * xyz[2] + JE * JE);
  JBE = asin(JE / BE);
  EBD = acos((BE * BE + BD2 - DE2) / (2 * BE * BD));
  BDE = acos((BD2 + DE2 - BE * BE) / (2 * DE * BD));

  ang[0] = asin(xyz[1] / FE);
  ang[1] = CBD + JBE + EBD - PI / 2;
  ang[2] = PI / 2 + CBD - BDE;
}


void FFK(float *ang, float *xyz)
{
    float AB = 53.05;
    float DE = 136.0;	
    float BD = 62.27585;
    float CBD = 0.22971;

    float GBD, BG, AG, DG, HDE, DH, HE, FE;

    GBD = ang[1] - CBD;
    BG = BD * cos(GBD);
    AG = AB + BG;
    DG = BD * sin(GBD);
    HDE = ang[1] - ang[2];
    DH = DE * cos(HDE);
    HE = DE * sin(HDE);
    FE = AG + HE;
    
    xyz[0] = FE * cos(ang[0]);
    xyz[1] = FE * sin(ang[0]);
    xyz[2] = DH - DG;
}


void currentToStart(float *arr)
{
    int i, j;
    float ang[18];
    float a[3], x[3];

    curPosition(ang);
    for(i = 0; i < 6; i++)
    {
        for(j = 0; j < 3; j++)
            a[j]=ang[i * 3 + j];

        FFK(a, x);

        for(j = 0; j < 3; j++)
            arr[i * 3 + j] = x[j];
    }
}


void moveStage()
{
    int i, j;
    float part;
    float a[3], x[3];

    part = float(millis() - startTime) / float(stageDuration);

    if(part < 1)
    {
        for(i = 0; i < 18; i++)
            xyzCur[i] = xyzStart[i] + (xyzFinish[i] - xyzStart[i]) * part;
    }
    else
    {
        readyToNextStage = true;
        for(i = 0; i < 18; i++)
            xyzCur[i] = xyzFinish[i];
    }

    for(i = 0; i < 6; i++)
    {
        for(j = 0; j < 3; j++)
            x[j] = xyzCur[i * 3 + j];

        IIK(x, a);

        for(j = 0; j < 3; j++)
            servoTurn(i * 3 + j + 1, a[j], 1023);
    }
}


void parkToGo() 
{     
    int i;

    if(stage == 5)
    {
        readyToChangeMode = true;
        mode = nextmode;
        gaitNo = 5;
        stage = 0;
        readyToNextStage = true;
    }

    if(stage == 4)
    {
        for(i = 0; i < 18; i++)
        {
            xyzStart[i] = xyzFinish[i];
            xyzCur[i] = xyzStart[i];
        }
        for(i = 1; i < 6; i+=2)
        {
            xyzFinish[i * 3] = 106;
            xyzFinish[i * 3 + 1] = 0;
            xyzFinish[i * 3 + 2] = 103;
        }            
        readyToNextStage = false;
        stage = 5;
        startTime = millis();
    }

    if(stage == 3)
    {
        for(i = 0; i < 18; i++)
        {
            xyzStart[i] = xyzFinish[i];
            xyzCur[i] = xyzStart[i];
        }
        for(i = 1; i < 6; i+=2)
        {
            xyzFinish[i * 3] = 135;
            xyzFinish[i * 3 + 1] = 0;
            xyzFinish[i * 3 + 2] = 80;
        }            
        readyToNextStage = false;
        stage = 4;
        startTime = millis();
    }

    if(stage == 2)
    {
        for(i = 0; i < 18; i++)
        {
            xyzStart[i] = xyzFinish[i];
            xyzCur[i] = xyzStart[i];
        }
        for(i = 0; i < 6; i+=2)
        {
            xyzFinish[i * 3] = 106;
            xyzFinish[i * 3 + 1] = 0;
            xyzFinish[i * 3 + 2] = 103;
        }            
        readyToNextStage = false;
        stage = 3;
        startTime = millis();
    }

    if(stage == 1)
    {
        for(i = 0; i < 18; i++)
        {
            xyzStart[i] = xyzFinish[i];
            xyzCur[i] = xyzStart[i];
        }
        for(i = 0; i < 6; i+=2)
        {
            xyzFinish[i * 3] = 135;
            xyzFinish[i * 3 + 1] = 0;
            xyzFinish[i * 3 + 2] = 80;
        }            
        readyToNextStage = false;
        stage = 2;
        startTime = millis();
    }

    if(stage == 0)
    {
        softSerial.println("Park To Go");
        currentToStart(xyzStart);
        for(i = 0; i < 6; i++)
        {
            xyzFinish[i * 3] = 163;
            xyzFinish[i * 3 + 1] = 0;
            xyzFinish[i * 3 + 2] = 103;
        }            
        for(i = 0; i < 18; i++)
            xyzCur[i] = xyzStart[i];
        readyToNextStage = false;
        stage = 1;
        startTime = millis();
    }
}


void goToPark() 
{     
    int i;

    if(stage == 5)
    {
        readyToChangeMode = true;
        mode = nextmode;
    }

    if(stage == 4)
    {
        for(i = 0; i < 18; i++)
        {
            xyzStart[i] = xyzFinish[i];
            xyzCur[i] = xyzStart[i];
        }
        for(i = 0; i < 6; i++)
        {
            xyzFinish[i * 3] = 163;
            xyzFinish[i * 3 + 1] = 0;
            xyzFinish[i * 3 + 2] = 35;
        }            
        readyToNextStage = false;
        stage = 5;
        startTime = millis();
    }

    if(stage == 3)
    {
        for(i = 0; i < 18; i++)
        {
            xyzStart[i] = xyzFinish[i];
            xyzCur[i] = xyzStart[i];
        }
        for(i = 1; i < 6; i+=2)
        {
            xyzFinish[i * 3] = 163;
            xyzFinish[i * 3 + 1] = 0;
            xyzFinish[i * 3 + 2] = 103;
        }            
        readyToNextStage = false;
        stage = 4;
        startTime = millis();
    }

    if(stage == 2)
    {
        for(i = 0; i < 18; i++)
        {
            xyzStart[i] = xyzFinish[i];
            xyzCur[i] = xyzStart[i];
        }
        for(i = 1; i < 6; i+=2)
        {
            xyzFinish[i * 3] = 135;
            xyzFinish[i * 3 + 1] = 0;
            xyzFinish[i * 3 + 2] = 80;
        }            
        readyToNextStage = false;
        stage = 3;
        startTime = millis();
    }

    if(stage == 1)
    {
        for(i = 0; i < 18; i++)
        {
            xyzStart[i] = xyzFinish[i];
            xyzCur[i] = xyzStart[i];
        }
        for(i = 0; i < 6; i+=2)
        {
            xyzFinish[i * 3] = 163;
            xyzFinish[i * 3 + 1] = 0;
            xyzFinish[i * 3 + 2] = 103;
        }            
        readyToNextStage = false;
        stage = 2;
        startTime = millis();
    }

    if(stage == 0)
    {
        softSerial.println("Park To Go");
        currentToStart(xyzStart);
        for(i = 0; i < 6; i+=2)
        {
            xyzFinish[i * 3] = 135;
            xyzFinish[i * 3 + 1] = 0;
            xyzFinish[i * 3 + 2] = 80;
        }            
        for(i = 0; i < 18; i++)
            xyzCur[i] = xyzStart[i];
        readyToNextStage = false;
        stage = 1;
        startTime = millis();
    }
}


void goToRad() 
{     
    int i;

    if (stage == 1)
    {
        readyToChangeMode = true;
        mode = nextmode;
        stageDuration = 500;
    }

    if(stage == 0)
    {
        softSerial.println("Park To Go");
        currentToStart(xyzStart);
        for(i = 0; i < 6; i++)
        {
            xyzFinish[i * 3] = 106;
            xyzFinish[i * 3 + 1] = 0;
            xyzFinish[i * 3 + 2] = 150;
        }            
        for(i = 0; i < 18; i++)
            xyzCur[i] = xyzStart[i];
        readyToNextStage = false;
        stage = 1;
        startTime = millis();
    }

}


void radToGo() 
{     
    int i;

    if (stage == 1)
    {
        readyToChangeMode = true;
        mode = nextmode;
    }

    if(stage == 0)
    {
        softSerial.println("Park To Go");
        currentToStart(xyzStart);
        for(i = 0; i < 6; i++)
        {
            xyzFinish[i * 3] = 106;
            xyzFinish[i * 3 + 1] = 0;
            xyzFinish[i * 3 + 2] = 103;
        }            
        for(i = 0; i < 18; i++)
            xyzCur[i] = xyzStart[i];
        readyToNextStage = false;
        stage = 1;
        startTime = millis();
    }
}


void mainGait()
{

}


void gait()
{
    int newGN = gaitNo;

    if(readyToChangeMode)
    {
        if(mode == 16 and nextmode == 8)
                newGN = 1; 
        if(mode == 8 and nextmode == 16)
                newGN = 2; 
        if(mode == 8 and nextmode == 2)
                newGN = 3; 
        if(mode == 2 and nextmode == 8)
                newGN = 4; 
    }
    
    if (gaitNo != newGN)
    {
        gaitNo = newGN;
        stage = 0;
        mode = 0;
        readyToChangeMode = false;
        readyToNextStage = true;
    }

    if (readyToNextStage)
    {
        if(gaitNo == 1)
            parkToGo();
        if(gaitNo == 2)
            goToPark();
        if(gaitNo == 3)
            goToRad();
        if(gaitNo == 4)
            radToGo();
        if(gaitNo == 5)
            mainGait();
    }
    else
        moveStage();
}


 