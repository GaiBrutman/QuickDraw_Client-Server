import java.net.*; 
import java.util.*;
import java.io.PrintStream;

color SUMMER_SKY = #1E8BC3;
color ABONY_GLAY = #22313F;
color WHITE_SMOKE = #ECECEC;
color BG_BLUE = #39a9db;

Socket mySocket;
Scanner sc;

boolean connected = false;    
boolean empty = true;
//boolean gotIt = false;

int port = 1235;
String temp = "";
String error = "";
String ip = null;
ArrayList<String> things;
String example = "Fish";

int count = 0;

int previewSize = 28*4;
int previewPad = 20;

PVector drawRectStart;
PVector drawRectEnd;

PVector mouse1;
PVector mouse2;
PVector min;
PVector max;

String thing;

float percentageProg = 0f;
float percentageAlpha = 1e-2;

String[] classes = new String[] {"", "", ""};
float[] preds = new float[] {0f, 0f, 0f};

float[] newPreds = new float[] {0f, 0f, 0f};

int penSize = 20;

PVector scaleV;

void setup() {
  fullScreen();
    
  scaleV = new PVector(width/1920., height/1200.);
  
  things = new ArrayList();
  
  drawRectStart = new PVector((previewSize+previewPad*2)*scaleV.x+60, 200*scaleV.y);
  drawRectEnd = new PVector(width-((previewSize+previewPad*2)*scaleV.x)-50, height-20*scaleV.y);
  
  mouse1 = new PVector(mouseX, mouseY);
  mouse2 = mouse1.copy();
  
  min = new PVector(width, height);
  max = new PVector(0, drawRectStart.y);
  
  eraseBoard(true);
}
 
void draw() {  
  if (connected) {
    drawAndPreview();
    
    if (frameCount % 20 == 0 && !empty && max.x > min.x + 20 && max.y > min.y + 20) {
      thread("comunicate");
    }
  } else if (!connected) {
    showConnecting();
  }
}

void keyPressed() {
  
  if (key == CODED) {
    if (keyCode == UP) {
      penSize = min(penSize+1, floor(100*scaleV.x));
    }
    if (keyCode == DOWN) {
      penSize = max(penSize-1, 1);
    }
  }
  
  if (key == ENTER && !connected) {
    ip = temp;
    startConnection();
  } else if (key == 'x') {
    eraseBoard(true);
  } else if (key == BACKSPACE) {
    if (temp != null && temp.length() > 0) {
        temp = temp.substring(0, temp.length() - 1);
        print("\n"+temp);
    }
  }
  else {
    temp += key;
    print(key);
  }
}
