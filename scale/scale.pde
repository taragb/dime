import processing.pdf.*;

int w = 690;
int h = 40;
int gap = 5;

int[] divisions = {10,20,30,50,90,100};

FloatDict points;

PFont font;


void setup() {
  //font = loadFont("Gotham-Light-32.vlw");
  createFont("Gotham", 12);
  size(1955,500, PDF, "scale.pdf");
  //size(500,500);
  background(255);
  
  smooth();
 
  noStroke();
  fill(110,200,192); 
  
  int startColor = color(217,239,235);
  int endColor = color(110,200,192);
  
  translate(50,50);
  float currentX = 0;
  for (int i = 0; i < divisions.length; i = i+1) {
    float currentWidth = 0;
    if(i == 0){
      currentWidth += (divisions[i]/100.0) * w;
    }
    else{
      currentWidth += (((divisions[i]/100.0) - (divisions[i-1]/100.0)) * w);
    }
    fill(lerpColor(startColor,endColor, i / float(divisions.length)));
    rect(currentX,0,currentWidth,h);
    currentX += currentWidth + gap;
  }
  fill(255);
  triangle(0,0,w,0,0,h/2);
  triangle(0,h/2,w,h,0,h);
  
  fill(254,201,93);
  rect(-3,0,6,30);
  ellipse(0,30,20,20);
  ellipse(0,-10,20,20);
  
  fill(0);
  currentX = 0;
  textAlign(CENTER);
  for (int i = 0; i < divisions.length; i = i+1) {
    float currentWidth = 0;
    if(i == 0){
      currentWidth += (divisions[i]/100.0) * w;
      text(0, currentX, 35);
    }
    else{
      currentWidth += (((divisions[i]/100.0) - (divisions[i-1]/100.0)) * w);
      text(divisions[i-1], currentX - 2, 35);
    }
    
    currentX += currentWidth + gap; 
  }
  
  exit();
}
