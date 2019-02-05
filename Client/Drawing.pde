void startDraw() {
  connected = true;
  eraseBoard(true);
}

void printKeys() {
  textAlign(LEFT, TOP);
  textSize(30*scaleV.y);
  
  fill(WHITE_SMOKE);
  
  text("Keys:\n\n[X]: Erase board\n[ESC]: Exit", 10, height/6);
}

void drawPenSize() {
  noStroke();
  fill(SUMMER_SKY);
  
  ellipse(floor(drawRectStart.x/2), floor(drawRectStart.y/2), floor(100*scaleV.x)+1, floor(100*scaleV.x)+1);
  fill(0);
  ellipse(floor(drawRectStart.x/2), floor(drawRectStart.y/2), penSize, penSize);
}

void drawAndPreview() {
  textAlign(LEFT, TOP);
  textSize(65*scaleV.y);
  
  fill(WHITE_SMOKE);
  
  text("BRUTMAN QUICK DRAW", drawRectStart.x, 10);
  printKeys();
  textSize(35*scaleV.y);
  
  text("Draw something, for example:\n" + example, drawRectStart.x, 10 + 80*scaleV.y);
  
  drawPenSize();
  
  mouse2 = mouse1.copy();
  mouse1.x = constrain(mouseX, drawRectStart.x+1, drawRectEnd.x-1);
  mouse1.y = constrain(mouseY, drawRectStart.y+1, drawRectEnd.y-1);
  //if (mousePressed)
    //println(min, max, drawRectStart, drawRectEnd);
  if (mousePressed && mouse1.x == mouseX && mouse1.y == mouseY) {
    empty = false;
    stroke(0);
    fill(0);
    strokeWeight(penSize);
    line(mouse1.x, mouse1.y, mouse2.x, mouse2.y);
    strokeWeight(1);
      
    if (mouse1.x < min.x)
      min.x = mouse1.x;
    if (mouse1.x > max.x)
      max.x = mouse1.x;
    if (mouse1.y < min.y)
      min.y = mouse1.y;
    if (mouse1.y > max.y)
      max.y = mouse1.y;
      
    if (!empty && max.x > min.x && max.y > min.y)
      showPreview();
  }
  
  int predsFullLength = floor(400*scaleV.x);
  
  showPreds(floor(drawRectEnd.x-predsFullLength), floor(10*scaleV.y), floor(drawRectStart.y/5), predsFullLength);
}

void showPreview() {
  PImage preview = getDrawing();
  
  int textSize = (int)((previewSize/(28*4.0))*30*scaleV.x);
  
  float previewX = drawRectEnd.x+20*scaleV.x;
  float previewY = drawRectStart.y+60*scaleV.y;
  
  int realPreviewSize = floor(width-drawRectEnd.x-20*scaleV.x*2);
  
  stroke(0);
  fill(0);
  
  textAlign(LEFT, BOTTOM);
  textSize(textSize);
  
  text("Preview", previewX, previewY);
  noFill();
  rect(previewX-1, previewY + 19, realPreviewSize+1, realPreviewSize+1);
  preview.resize(realPreviewSize, realPreviewSize);
  image(preview, previewX, previewY + 20);
}

void showMessages() {
  
  fill(SUMMER_SKY);
  noStroke();
  rect(0, 0, width, drawRectStart.y);
  
  textAlign(CENTER, CENTER);
  textSize(30);
  fill(WHITE_SMOKE);
  stroke(WHITE_SMOKE);
}

void eraseBoard(boolean eraseAll) {
  empty = true;
  min = new PVector(width, height);
  max = new PVector();
  
  
  if (eraseAll) {
    background(SUMMER_SKY);
  }
  
  strokeWeight(1);
  stroke(0);
  fill(255);
  rect(drawRectStart.x, drawRectStart.y, drawRectEnd.x-drawRectStart.x, drawRectEnd.y-drawRectStart.y); 
}

void textWithOutline(String s, float x, float y, color c, color outC, int n) {
  fill(outC);
    
  for(int i = -n; i < n+1; i++){
    text(s, x+i, y);
    text(s, x, y+i);
  }
    
  fill(c);
  text(s, x, y);
}
