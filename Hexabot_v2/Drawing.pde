import controlP5.*;
ControlP5 cp5;
Textfield[][] angcoor=new Textfield[6][3];
Textfield[][] deccoor=new Textfield[6][3];
Textfield voltcp;
Slider2D slider;
Slider sld;

Toggle gaitsw;

// Robot parameters
int body_ln=244;
int body_wdth=134;
int body_rl=195;
int body_hgh=40;
int coxa=53;
int femur=83;
int tibia=140;
int shiftX=500;
int shiftY=400;

int floor=100;
int leg_ln=141;

void drawLeg(float alfa, float beta, float gamma)
{
  sphere(20);
  rotateY(alfa);
  translate(float(coxa)/4, 0, 0);
  box(float(coxa)/2,50,20);
  translate(float(coxa)/2, 0, 0);
  box(float(coxa)/2,20,50);
  translate(float(coxa)/4, 0, 0);
  sphere(20);
  rotateZ(beta);
  translate(float(femur)/2,0,0);
  box(femur,20,20);
  translate(float(femur)/2,0,0);
  sphere(20);
  rotateZ(gamma);
  translate(float(tibia+10)/2-30,0,0);
  box(tibia+10,10,40);
  translate(float(tibia+10)/2,0,0);
  rotateX(PI/2);
  rotateZ(PI/4);
  box(40/sqrt(2),40/sqrt(2),2);
}

void drawRobot()
{
  float Z, X, R;
  
  pushMatrix();
    translate(shiftX, shiftY, sld.getValue());
    rotateX(-slider.getArrayValue()[1]);
    rotateY(slider.getArrayValue()[0]);
    box(body_ln, body_hgh, body_wdth);
    pushMatrix();
      translate(0, floor, 0);
      strokeWeight(4);
      line(-300,0,body_rl/2+leg_ln,300,0,body_rl/2+leg_ln);
      line(-300,0,-body_rl/2-leg_ln,300,0,-body_rl/2-leg_ln);
      line(0,0,-300,0,0,300);
      Z=(float)body_wdth/2+(float)leg_ln/sqrt(2);
      line(-300,0,Z,300,0,Z);
      line(-300,0,-Z,300,0,-Z);
      X=(float)body_ln/2+(float)leg_ln/sqrt(2);
      line(-X,0,-300,-X,0,300);
      line(X,0,-300,X,0,300);
      R=2*sqrt(X*X+Z*Z);
      rotateX(PI/2);
      noFill();
      ellipse(0,0,body_rl+2*leg_ln,body_rl+2*leg_ln);
      ellipse(0,0,R,R);
      fill(255);
      strokeWeight(1);
    popMatrix();
    pushMatrix();
      rotateY(PI/4);
      box(float(body_rl)/sqrt(2), body_hgh-2, float(body_rl)/sqrt(2));
    popMatrix();
    for(int i=0; i<6; i++)
    {
      pushMatrix();
        translate((1-floor(i/2))*body_ln/2, 0, -1*(1-(i%2)*2)*((1-floor(i/2))==0?body_rl:body_wdth)/2);
        rotateY((1-(i%2)*2)*(floor(i/2)+1)*PI/4);
        pushMatrix();
          fill(0);
          textSize(30);
          text(str(i+1),-30,-22,0);
          fill(255);
        popMatrix();
        drawLeg(ang[i][0], ang[i][1], ang[i][2]);
      popMatrix();
    }
  popMatrix();
}

void setupControls()
{
  cp5 = new ControlP5(this);

  for(int i=0; i<6; i++)
    for(int j=0; j<3; j++)
    {
      angcoor[i][j] = cp5.addTextfield("Ang"+str(i)+str(j))
        .setPosition(20+i*60, 20+j*25)
        .setSize(50,20)
        .setCaptionLabel("");
      deccoor[i][j] = cp5.addTextfield("Dec"+str(i)+str(j))
        .setPosition(450+i*60, 20+j*25)
        .setSize(50,20)
        .setCaptionLabel("");
      angcoor[i][j].setText("0");
    }
    
  voltcp=cp5.addTextfield("Height")
    .setPosition(930, 20)
    .setSize(30,20)
    .align(ControlP5.CENTER, ControlP5.CENTER, ControlP5.CENTER, ControlP5.TOP_OUTSIDE);
  
  slider=cp5.addSlider2D("Slider")
    .setPosition(450,700)
    .setSize(100,100)
    .setMinMax(-PI,-PI,PI,PI)
    .setValue(-PI/6,PI/6);
         
  sld=cp5.addSlider("Slider2")
    .setPosition(570,700)
    .setSize(20,100)
    .setRange(-300,300);
     
  cp5.addButton("Set")
    .setPosition(880,20)
    .setSize(40,20)
    .align(ControlP5.CENTER, ControlP5.CENTER, ControlP5.CENTER, ControlP5.CENTER); 

  gaitsw=cp5.addToggle("Gait")
    .setPosition(830,20)
    .setSize(40,20)
    .align(ControlP5.CENTER, ControlP5.CENTER, ControlP5.CENTER, ControlP5.CENTER); 

  cp5.addButton("AtoD")
    .setPosition(390,20)
    .setSize(40,20)
    .align(ControlP5.CENTER, ControlP5.CENTER, ControlP5.CENTER, ControlP5.CENTER); 

  cp5.addButton("DtoA")
    .setPosition(390,70)
    .setSize(40,20)
    .align(ControlP5.CENTER, ControlP5.CENTER, ControlP5.CENTER, ControlP5.CENTER); 
}