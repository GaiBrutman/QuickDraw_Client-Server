void startConnection() {
  try {
    println();
    ip = temp;
    mySocket = new Socket(ip, port);
    println("socket");
    sc = new Scanner(mySocket.getInputStream());
    println("scanner");
    
    example = recvLine();
    
    startDraw();

  } catch (UnknownHostException e) {
    ip = null;
    temp = "";
    println("HOST ERROR");
    error = "HOST ERROR";
  } catch (IOException e) {
    ip = null;
    temp = "";
    println("IO ERROR");
    error = "IO ERROR";
  }
}

void showConnecting() {
  background(255);
  fill(0);
  textAlign(CENTER, BOTTOM);
  textSize(60);
  text("SERVER IP - "+temp, width/2, 100*scaleV.y);
  
  fill(255, 0, 0);
  textWithOutline(error, width/2, 100+60*scaleV.y, color(255, 0, 0), 0, 2);
  //text(error, width/2, 100+60*scaleV.y);
}

void send(String s) {
  try {
    PrintStream p = new PrintStream(mySocket.getOutputStream());
    p.print(s);
  } catch (IOException e){
    println("IO ERROR");
  }
}

void sendCuncks(String s) {
  send(s);
  if (s.length() <= 20)
    println("sending " + s);
  else
    println("sending " + s.substring(0, 20) + "...");
  send("!@#");
}

String recvLine() {
  try {
    String s = null;
    s = sc.nextLine();
    println("recieved " + s.substring(0, min(s.length(), 20)));
    return s;
  } catch (java.util.NoSuchElementException e){
    println(e);
    exit();
    return "";
  }
}

void sendImage() {
  String imgStr = Img2Str();
  
  sendCuncks(imgStr);
  
  count++;
}

void getPrecentagePrediction() {
  String prediction = recvLine();
  
  String[] commaSplit = prediction.split(",");

  classes = new String[commaSplit.length];
  preds = new float[commaSplit.length];
  
  for (int i = 0; i < commaSplit.length; i++) {
    String[] colonSplit = commaSplit[i].split(":");
    
    classes[i] = colonSplit[0];
    preds[i] = float(colonSplit[1]);
  }
  if (percentageProg == 1)
    percentageProg = 0f;
}

void comunicate() {
  sendImage();
  getPrecentagePrediction();
}