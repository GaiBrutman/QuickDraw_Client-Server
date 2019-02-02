PImage getDrawing() {
  PVector corner1 = min.copy();
  PVector corner2 = max.copy();
    
  int padX;
  int padY;
  
  float offset = abs((max.x - min.x) - (max.y - min.y));
  float pad;
  if (abs(max.x - min.x) > abs(max.y - min.y)){
    pad = abs(max.x - min.x)/6;
    
    padX = (int)pad;
    padY = (int)(offset/2 + pad);
  } else {
    pad = (max.y - min.y)/4;
    
    padX = (int)(offset/2 + pad);
    padY = (int)pad;
  }
    
  int _width = int(abs(corner2.x-corner1.x));
  int _height = int(abs(corner2.y-corner1.y));
  
  PImage screenImg = get(int(corner1.x), int(corner1.y), _width, _height);
  
  PImage padded_img = createImage(screenImg.width + padX*2, screenImg.height + padY*2, RGB);
  padded_img.filter(INVERT);
  
  padded_img.copy(screenImg, 0, 0, screenImg.width, screenImg.height, 
                      padX, padY, screenImg.width, screenImg.height);
  
  padded_img.resize(28, 28);
  
  int darkestPixel = 255;
  padded_img.loadPixels();
  for (int i = 0; i < padded_img.pixels.length; i++) {
    if (brightness(padded_img.pixels[i]) < brightness(darkestPixel)) {
      darkestPixel = padded_img.pixels[i];
    }
  }
  float factor = 255 / (255.0001- (brightness(darkestPixel)));
  
  for (int i = 0; i < padded_img.pixels.length; i++) {
    float a = constrain(255 - ((255-brightness(padded_img.pixels[i])) * factor), 0, 255);
    padded_img.pixels[i] = color(a, a, a);
  }
  padded_img.updatePixels();
  
  return padded_img;
}

String Img2Str() {
  PImage img = getDrawing();
  
  String str = "";
  for (int i = 0; i < img.pixels.length; i++) {
    str += 255-int(brightness(color(img.pixels[i])));
    if (i < img.pixels.length-1)
      str += " ";
  }
  
  return str;
}