// coxa  -120 : 120
// femur    0 : 340
// tibia -500 : 300

boolean angdec=true;

int stage=0;
int step_ln=0;
int step_stf=0;
float ang_trn=0;
int step_hgh=0;
int gait_sp=250;
float hg;
float leg;
float leg2;
float rb;
float rs;
float X, Y;

int tm;
int curtm;
boolean motion=false;

float[][] decfrom=new float[6][3];
float[][] deccur=new float[6][3];
float[][] decto=new float[6][3];
float[][] angfrom=new float[6][3];
float[][] angto=new float[6][3];
float[][] angcur=new float[6][3];

char motype='n';

void keyPressed()
{
  if(key=='r')
    gait_sp+=100;

  if(key=='f')
  {
    gait_sp-=100;
    if(gait_sp<50)
      gait_sp=50;
  }
  
  if(key=='w')
  {
    step_ln+=30;
    if(step_ln>30)
      step_ln=30;
  }

  if(key=='s')
  {
    step_ln-=30;
    if(step_ln<-30)
      step_ln=-30;
  }
  
  if(key=='d')
  {
    step_stf+=30;
    if(step_stf>30)
      step_stf=30;
  }
  
  if(key=='a')
  {
    step_stf-=30;
    if(step_stf<-30)
      step_stf=-30;
  }
  
  if(key=='q')
  {
    ang_trn+=10;
    if(ang_trn>10)
      ang_trn=10;
  }
  
  if(key=='e')
  {
    ang_trn-=10;
    if(ang_trn<-10)
      ang_trn=-10;
  }
  
  if((step_ln|step_stf|round(ang_trn))==0)
    step_hgh=0;
  else
    step_hgh=30;

}

void Set()
{
  float hgh;
  float AB, BC, CE, CD, CBD, AD, AD2;

  if(gaitsw.getState())
    return;

  hgh=float(voltcp.getText());
  AB=(float)coxa;
  BC=(float)femur;
  CE=(float)tibia;
  
  CD=CE-hgh;
  CBD=asin(CD/BC);
  AD=AB+BC*cos(CBD);
  AD2=AD/sqrt(2);
  
  globdec[0][0]=AD2;
  globdec[1][0]=AD2;
  globdec[2][0]=AD;
  globdec[3][0]=AD;
  globdec[4][0]=AD2;
  globdec[5][0]=AD2;
  globdec[0][1]=AD2;
  globdec[1][1]=AD2;
  globdec[2][1]=0;
  globdec[3][1]=0;
  globdec[4][1]=-AD2;
  globdec[5][1]=-AD2;
  for(int i=0; i<6; i++)
    globdec[i][2]=hgh;
  
  for(int i=0; i<6; i++)
    for(int j=0; j<3; j++)
      deccoor[i][j].setText(str((float)round(globdec[i][j]*10000)/10000));
  
  DtoA();
  
  floor=round(hgh);
  leg_ln=round(AD);
 
  hg=hgh;
  leg=AD;
  leg2=AD2;
  
  X=(float)body_wdth/2+leg2;
  Y=(float)body_ln/2+leg2;
  rb=sqrt(X*X+Y*Y);
  rs=(float)body_rl/2+leg;
}

void Gait()
{
  if(gaitsw.getState())
    motype='g';
  else
    motype='n';
}

void Moving()
{
  int i,j;
  float alfa, alfas, xs, ys, xb, yb, xbm, ybm;
  
  if(motype!='n')
  {
    if(motion)
    {
      curtm=millis()-tm;
      if(curtm<gait_sp)
        for(i=0;i<6;i++)
          for(j=0;j<3;j++)
            if(angdec)
              angcur[i][j]=round(angfrom[i][j]+(angto[i][j]-angfrom[i][j])*((float)curtm/gait_sp));    
            else
              deccur[i][j]=round(decfrom[i][j]+(decto[i][j]-decfrom[i][j])*((float)curtm/gait_sp));    
      else
      {
        for(i=0;i<6;i++)
          for(j=0;j<3;j++)
            if(angdec)
              angcur[i][j]=angto[i][j];
            else
              deccur[i][j]=decto[i][j];
        motion=false;
        stage++;
        if(stage==4) 
          stage=0;
      }
      for(i=0; i<6; i++)
        for(j=0; j<3; j++)
          if(angdec)
            angcoor[i][j].setText(str(angcur[i][j]));
          else
            deccoor[i][j].setText(str(int(deccur[i][j])));
      if(angdec)
        AtoD();
      else
        DtoA();
    }
    else
    {
      tm=millis();
      for(i=0;i<6;i++)
        for(j=0;j<3;j++)
          decfrom[i][j]=globdec[i][j];
          
      alfa=asin(X/rb);
      alfas=alfa+ang_trn/180*PI;
      xb=sin(alfas)*rb-X;
      yb=cos(alfas)*rb-Y;
      alfas=alfa-ang_trn/180*PI;
      xbm=sin(alfas)*rb-X;
      ybm=cos(alfas)*rb-Y;
      
      xs=cos(ang_trn/180*PI)*rs-rs;
      ys=sin(ang_trn/180*PI)*rs;
      
      switch(stage)
      {
        case 0:
          decto[0][0]=leg2;
          decto[1][0]=leg2;
          decto[2][0]=leg;
          decto[3][0]=leg;
          decto[4][0]=leg2;
          decto[5][0]=leg2;
          decto[0][1]=leg2;
          decto[1][1]=leg2;
          decto[2][1]=0;
          decto[3][1]=0;
          decto[4][1]=-leg2;
          decto[5][1]=-leg2;
          decto[0][2]=hg-step_hgh;
          decto[1][2]=hg;
          decto[2][2]=hg;
          decto[3][2]=hg-step_hgh;
          decto[4][2]=hg-step_hgh;
          decto[5][2]=hg;
          motion=true;
          break;
        case 1:
          decto[0][0]=leg2+step_stf+xb;
          decto[1][0]=leg2+step_stf+xb;
          decto[2][0]=leg-step_stf+xs;
          decto[3][0]=leg-step_stf+xs;
          decto[4][0]=leg2+step_stf+xbm;
          decto[5][0]=leg2+step_stf+xbm;
          decto[0][1]=leg2+step_ln+yb;
          decto[1][1]=leg2-step_ln+yb;
          decto[2][1]=0-step_ln+ys;
          decto[3][1]=0+step_ln+ys;
          decto[4][1]=-leg2+step_ln-ybm;
          decto[5][1]=-leg2-step_ln-ybm;
          decto[0][2]=hg;
          decto[1][2]=hg;
          decto[2][2]=hg;
          decto[3][2]=hg;
          decto[4][2]=hg;
          decto[5][2]=hg;
          motion=true;
          break;
        case 2:
          decto[0][0]=leg2;
          decto[1][0]=leg2;
          decto[2][0]=leg;
          decto[3][0]=leg;
          decto[4][0]=leg2;
          decto[5][0]=leg2;
          decto[0][1]=leg2;
          decto[1][1]=leg2;
          decto[2][1]=0;
          decto[3][1]=0;
          decto[4][1]=-leg2;
          decto[5][1]=-leg2;
          decto[0][2]=hg;
          decto[1][2]=hg-step_hgh;
          decto[2][2]=hg-step_hgh;
          decto[3][2]=hg;
          decto[4][2]=hg;
          decto[5][2]=hg-step_hgh;
          motion=true;
          break;
        case 3:
          decto[0][0]=leg2-step_stf+xbm;
          decto[1][0]=leg2-step_stf+xbm;
          decto[2][0]=leg+step_stf+xs;
          decto[3][0]=leg+step_stf+xs;
          decto[4][0]=leg2-step_stf+xb;
          decto[5][0]=leg2-step_stf+xb;
          decto[0][1]=leg2-step_ln+ybm;
          decto[1][1]=leg2+step_ln+ybm;
          decto[2][1]=0+step_ln-ys;
          decto[3][1]=0-step_ln-ys;
          decto[4][1]=-leg2-step_ln-yb;
          decto[5][1]=-leg2+step_ln-yb;
          decto[0][2]=hg;
          decto[1][2]=hg;
          decto[2][2]=hg;
          decto[3][2]=hg;
          decto[4][2]=hg;
          decto[5][2]=hg;
          motion=true;
          break;
      }   

      if(angdec)
      {
        for(i=0; i<6; i++)
          for(j=0; j<3; j++)
            globdec[i][j]=decto[i][j];
        GlobToLoc();
        CalcTick();
        for(i=0; i<6; i++)
          for(j=0; j<3; j++)
            angto[i][j]=tick[i][j];
      
        for(i=0; i<6; i++)
          for(j=0; j<3; j++)
            globdec[i][j]=decfrom[i][j];
        GlobToLoc();
        CalcTick();
        for(i=0; i<6; i++)
          for(j=0; j<3; j++)
            angfrom[i][j]=tick[i][j];
      }
    }
  }
  else
  {
    stage=0;
    motion=false;
  }
}