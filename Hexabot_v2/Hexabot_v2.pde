void setup() 
{
  size(1000, 800, P3D);

  setupControls();

  voltcp.setText("100");
  Set();
}

void draw()
{
  background(128);

  Moving();

  getAng();

  drawRobot();
}