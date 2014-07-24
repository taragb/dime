import processing.pdf.*;

JSONArray json;

PShape icn;
PShape star;

PFont boldFont;
PFont lightFont;

Table data;

//dimensions
int w = 1955;
int h = 2806;

//colors
int primaryColor = color(94,174,164);
int secondaryColor = color(111,200,192);
int highlightColor = color(254,201,94);
int textColor = color(0);

void setup(){
  
  background(255);
  fill(0);
  size(w, h, PDF, "size.pdf");
  
  //LOAD DATA
  json = loadJSONArray("tabulated_data.json");
  JSONObject first = json.getJSONObject(0);
  
  JSONArray sections = first.getJSONArray("items");
  
  
  for (int i = 0; i < sections.size(); i++) {
    JSONObject section = sections.getJSONObject(i); 
    String title = section.getString("label");
    println(title);
  }
  
  boldFont = createFont("GillSans-Bold",93);
  lightFont = createFont("GillSans-Light",50);
  
  textFont(boldFont);
  
  
  //SECTION: Title

  fill(primaryColor);
  text(first.getString("label"), 77, 100);
  
  fill(textColor);
  textFont(lightFont);
  text("CAPACITÉ INSTITUTIONELLE", 77, 200);
  text("MUNICIPALITÉ DE ", 1020, 200);
  
  //three dots
  noStroke();
  fill(highlightColor);
  for (int i = 0; i < 3; i = i+1) {
    ellipse(830 + (i * 80), 180, 22, 22);
  }
  
  //SECTION: MAIRIE/SERVICES MUNICIPAUX
  
  sectionHeader(249, "building.svg", sections.getJSONObject(0).getString("label"),sections.getJSONObject(0).getFloat("points"),sections.getJSONObject(0).getFloat("max_points"));
  sectionHeader(938, "council.svg", sections.getJSONObject(1).getString("label"),sections.getJSONObject(1).getFloat("points"),sections.getJSONObject(1).getFloat("max_points"));
  sectionHeader(1795, "coins.svg", sections.getJSONObject(2).getString("label"),sections.getJSONObject(2).getFloat("points"),sections.getJSONObject(2).getFloat("max_points"));
  
  exit();

}

//Section header template
void sectionHeader(int yPos, String iconPath, String title, float points, float max){
  
  icn = loadShape(iconPath);
  
  fill(secondaryColor);
  noStroke();
  rect(65,yPos, 1590, 96);
  
  stroke(primaryColor);
  fill(255);
  strokeWeight(9);
  
  line(65,yPos,1638,yPos);
  
  ellipse(136,97 + yPos,246,246);
  shape(icn, 26, 10 + yPos);
  
  fill(255);
  noStroke();
  beginShape();
  vertex(1637,yPos - 10);
  vertex(1700,yPos - 10);
  vertex(1650,yPos + 100);
  vertex(1587,yPos + 100);
  endShape();
  
  textFont(boldFont);
  textSize(48);
  float tw = textWidth(title);
  text(title, 290, yPos + 65);
  
  textFont(lightFont);
  textSize(42);
  text("— " + points + "/" + max + " points", tw + 310, yPos + 60);
  
  
  //FIXME: Figure out the correct star mapping
  stars(round(points/max * 3), yPos);
  
}

//Stars for section ratings
void stars(int rating, int yPos){
  fill(0);
  int gap = 100;
  star = loadShape("star.svg");
  star.disableStyle();
  
  for (int i = 0; i < 3; i = i+1) {
    
    if(i < rating){
      fill(primaryColor);
    }
    else{
      fill(primaryColor, 30);
    }
    shape(star, gap * i + 1640, yPos + 15);
    
  }
}

void scale(){
  
  
}
