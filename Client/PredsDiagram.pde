
void showPreds(int startX, int startY, int size, int fullLen) {
  
  fill(SUMMER_SKY);
  noStroke();
  rect(startX, startY, fullLen, size*((classes.length-1)*1.5+1.2));
  
  if (newPreds.length != preds.length) {
    newPreds = new float[preds.length];
  }
  
  for (int i = 0; i < preds.length; i++) {  
    float corrPred = map(percentageProg, 0, 1, newPreds[i], preds[i]);
        
    noStroke();
    fill(0, 255, 0);
    rect(startX, startY+i*size*1.5, fullLen*corrPred/100, 1.2*size);
    
    stroke(0);
    noFill();
    rect(startX, startY+i*size*1.5, fullLen, 1.2*size);
    
        
    textAlign(LEFT, TOP);
    textSize(size);
    
    float x = startX+10, y = startY+i*size*1.5;
    
    textWithOutline(classes[i] + ": " + int(corrPred) + "%", x, y, WHITE_SMOKE, 0, 1);
    
    if (percentageProg == 1) {
      newPreds[i] = preds[i];
    }
    percentageProg = min(percentageProg+percentageAlpha, 1);
  }
}