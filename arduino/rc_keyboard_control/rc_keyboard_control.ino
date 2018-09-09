int right_pin = 5;
int left_pin = 7;
int forward_pin = 11;
int reverse_pin = 9;

int command = 0;
int time = 30;

void setup() {
  pinMode(right_pin, OUTPUT);
  pinMode(left_pin, OUTPUT);
  pinMode(forward_pin, OUTPUT);
  pinMode(reverse_pin, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  if(Serial.available()){
    command = Serial.read();
  }
  else{
    reset();
  }
  drive(command);

}

void reset(){
  //Setting all pins to high makes sure the car doesn't move
  digitalWrite(right_pin, HIGH);
  digitalWrite(left_pin, HIGH);
  digitalWrite(forward_pin, HIGH);
  digitalWrite(reverse_pin, HIGH);
}

void forward(int time){
  Serial.println("forward");
  digitalWrite(forward_pin, LOW);
  delay(200);
}

void reverse(int time){
  Serial.println("reverse");
  digitalWrite(reverse_pin, LOW);
  delay(time);

}

void left(int time){
  Serial.println("left");
  digitalWrite(left_pin, LOW);
  delay(time);
}

void right(int time){
  Serial.println("right");
  digitalWrite(right_pin, LOW);
  delay(time);
}

void forward_right(int time){
  Serial.println("forward right");
  digitalWrite(forward_pin, LOW);
  digitalWrite(right_pin, LOW);
  delay(time);
}

void reverse_right(int time){
  Serial.println("reverse right");
  digitalWrite(reverse_pin, LOW);
  digitalWrite(right_pin, LOW);
  delay(time);
}

void forward_left(int time){
  Serial.println("forward left");
  digitalWrite(forward_pin, LOW);
  digitalWrite(left_pin, LOW);
  delay(time);
}

void reverse_left(int time){
  Serial.println("reverse left");
  digitalWrite(reverse_pin, LOW);
  digitalWrite(left_pin, LOW);
  delay(time);

}


void drive(int command){
  switch(command){
     case 0: reset(); break;
     case 1: forward(time); break;
     case 2: reverse(time); break;
     case 3: right(time); break;
     case 4: left(time); break;
     case 5: forward_right(time); break;
     case 6: forward_left(time); break;
     case 7: reverse_right(time); break;
     case 8: reverse_left(time); break;

     default: Serial.print("Invalid Command\n");
  }
}

