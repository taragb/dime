import processing.pdf.*;

//int w = 690;
int w = 400;
int h = 20;
int gap = 0;

int[] divisions = {20,40,60,80,90,100};

int[] points = {0,1,4,6,8,10};
int[] pointLocations = {20,40,60,80,90,100};

PFont font;
PFont bold;

Table data;

void setup() {
  //font = loadFont("Gotham-Light-32.vlw");
  //createFont("Gotham", 32);
  size(500,100, PDF, "scale.pdf");
  //size(500,500);
  background(255);
  
  smooth();
 
  noStroke();
  
  data = loadTable("tabulated_data.csv", "header");
  println(data.getRowCount() + " total rows in table");
  
  PGraphicsPDF pdf = (PGraphicsPDF) g;  // Get the renderer
  
  for (TableRow row : data.rows()) {
    
    String commune = row.getString("commune");
    int attendance = row.getInt("average_attendance");
    
    fill(0);
    textAlign(LEFT);
    text(commune, 5, 15);
    
    if(attendance > 100){
      attendance = 100;
    }

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
  rect(((attendance/100.0) * w) -3,0,6,30);
  ellipse((attendance/100.0) * w,30,20,20);
  ellipse((attendance/100.0) * w,-10,20,20);
  
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
      
      if(i + 1 == divisions.length){
        text(divisions[i-1], currentX - 2, 35);
      }
      else{
        text(divisions[i-1], currentX - 2, 35);
      }
    }
    
    currentX += currentWidth + gap; 
  }
  
  bold = loadFont("Gotham-Bold-32.vlw");
  currentX = 0;
  for (int i = 0; i < points.length; i = i+1) {
    float currentWidth = 0;
    if(i == 0){
      currentWidth += (pointLocations[i]/100.0) * w;
      text(0, currentX, -5);
    }
    else{
      currentWidth += (((pointLocations[i]/100.0) - (pointLocations[i-1]/100.0)) * w);
      
      if(i + 1 == points.length){
        text(points[i] + " pts.", currentX - 2, -5);
      }
      else{
        text(points[i], currentX - 2, -5);
      }
    }
    
    currentX += currentWidth + gap; 
  }
  //ugly
  text("100%", w + (gap*divisions.length), 35);
  
  pdf.nextPage();  // Tell it to go to the next page
  }
  exit();
}
