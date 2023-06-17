int[][] dir={{1, 1,-1},
             {1,-1, 1},
             {1, 1,-1},
             {1, 1,-1},
             {1,-1, 1},
             {1, 1,-1}}; 
float[][] gloc={{-1, -PI/4},
                { 1,  PI/4},
                {-1,     0},
                { 1,     0},
                {-1,  PI/4},
                { 1, -PI/4}};
                
float[][] tick=new float[6][3];
float[][] ang=new float[6][3];
float[][] locdec=new float[6][3];
float[][] globdec=new float[6][3]; 

void AtoD()
{
  for(int i=0; i<6; i++)
    for(int j=0; j<3; j++)
      tick[i][j]=float(angcoor[i][j].getText());
  CalcLocDec();
  LocToGlob();
  for(int i=0; i<6; i++)
    for(int j=0; j<3; j++)
      deccoor[i][j].setText(str((float)round(globdec[i][j]*10000)/10000));
}

void DtoA()
{
  for(int i=0; i<6; i++)
    for(int j=0; j<3; j++)
      globdec[i][j]=float(deccoor[i][j].getText());
  GlobToLoc();
  CalcTick();
  for(int i=0; i<6; i++)
    for(int j=0; j<3; j++)
      angcoor[i][j].setText(str((float)round(tick[i][j]*10000)/10000));
}

void CalcLocDec()
{
  int i;
  float AB, BC, CD, CoBC, FeCD, BCD, BD, CBD, CDB, BBD, BB, BsD, DDz, DDr, Alfa; 
  
  AB=(float)coxa;
  BC=(float)femur;
  CD=(float)tibia;
  
  for(i=0; i<6; i++)
  {
    CoBC=tick[i][1]/1024.0*300.0/180.0*PI;
    FeCD=tick[i][2]/1024.0*300.0/180.0*PI;
    BCD=PI+FeCD;
    BD=sqrt(BC*BC+CD*CD-2*BC*CD*cos(BCD));
    CDB=asin(BC*sin(BCD)/BD);
    CBD=PI-CDB-BCD;
    BBD=CoBC-CBD+PI/2;
    BB=BD*cos(BBD);
    BsD=abs(BD*sin(BBD));
    DDz=AB+BsD;
    DDr=BB;
    Alfa=tick[i][0]/1024.0*300.0/180.0*PI;
    locdec[i][0]=DDz*cos(Alfa);
    locdec[i][1]=DDz*sin(Alfa);
    locdec[i][2]=DDr;  
  }
}

void getAng()
{
  for(int i=0; i<6; i++)
    for(int j=0; j<3; j++)
      ang[i][j]=((j==0)?1:-1)*300.0/1024.0*float(angcoor[i][j].getText())/360*2*PI;
}  

void CalcTick()
{
  int i;
  float AB, BC, CD, DDz, Alfa, BsD, BD, BBD, CBD, CoBC, BCD; 
  
  AB=(float)coxa;
  BC=(float)femur;
  CD=(float)tibia;
  
  for(i=0; i<6; i++)
  {
    DDz=sqrt(locdec[i][0]*locdec[i][0]+locdec[i][1]*locdec[i][1]);
    Alfa=asin(locdec[i][1]/DDz);
    BsD=DDz-AB;
    BD=sqrt(BsD*BsD+locdec[i][2]*locdec[i][2]);
    BBD=acos(locdec[i][2]/BD);
    CBD=acos((BC*BC+BD*BD-CD*CD)/(2*BC*BD));
    CoBC=BBD+CBD-PI/2;
    BCD=acos((BC*BC+CD*CD-BD*BD)/(2*BC*CD));
    tick[i][0]=Alfa/PI*180.0/300.0*1024.0;
    tick[i][1]=CoBC/PI*180.0/300.0*1024.0;
    tick[i][2]=(BCD-PI)/PI*180.0/300.0*1024.0;
  }
}

void LocToGlob()
{
  float r, ang;
  for(int i=0; i<6; i++)
  {
    r=sqrt(locdec[i][0]*locdec[i][0]+locdec[i][1]*locdec[i][1]);
    ang=asin(locdec[i][1]/r);
    ang=ang+gloc[i][1];
    globdec[i][0]=r*cos(ang);
    globdec[i][1]=gloc[i][0]*r*sin(ang);  
    globdec[i][2]=locdec[i][2];  
  }
}

void GlobToLoc()
{
  float r, ang;
  for(int i=0; i<6; i++)
  {
    r=sqrt(globdec[i][0]*globdec[i][0]+globdec[i][1]*globdec[i][1]);
    ang=asin(gloc[i][0]*globdec[i][1]/r);
    ang=ang-gloc[i][1];
    locdec[i][0]=r*cos(ang);
    locdec[i][1]=r*sin(ang);  
    locdec[i][2]=globdec[i][2];  
  }
}