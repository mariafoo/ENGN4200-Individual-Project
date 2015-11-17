int xAxis = A0; 
int yAxis = A1; 
int zAxis = A2; 
int axisValue = 0;

int ledPins;

void setup() {
  Serial.begin(9600);
  Serial.println("Starting up");
  
  pinMode(ledPins = 11, OUTPUT); // pin 11 (on-board LED) as OUTPUT
  pinMode(ledPins = 12, OUTPUT); // pin 12 (on-board LED) as OUTPUT
  pinMode(ledPins = 13, OUTPUT); // pin 13 (on-board LED) as OUTPUT
}

void loop() {
  axisValue = analogRead(xAxis);
  Serial.print("X=");
  Serial.print(axisValue); 

  if(axisValue > 300) {
    digitalWrite(ledPins = 11, HIGH);
    //Serial.println("A");
  }
  else {
    digitalWrite(ledPins = 11, LOW);
    //Serial.println("C");
  }

  axisValue = analogRead(yAxis);
  Serial.print(",Y=");
  Serial.print(axisValue);

  if(axisValue > 300) {
    digitalWrite(ledPins = 12, HIGH);
    //Serial.println("A");
  }
  else {
    digitalWrite(ledPins = 12, LOW);
    //Serial.println("C");
  }

  axisValue = analogRead(zAxis);
  Serial.print(",Z=");
  Serial.println(axisValue);

  if(axisValue > 300) {
    digitalWrite(ledPins = 13, HIGH);
    //Serial.println("A");
  }
  else {
    digitalWrite(ledPins = 13, LOW);
    //Serial.println("C");
  }
  delay(200);
}
