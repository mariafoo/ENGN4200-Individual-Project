int xAxis = A0; 
int yAxis = A1; 
int zAxis = A2; 
int axisValue = 0;

unsigned long time;

void setup() {
  Serial.begin(9600);
  // block until the current transmit buffer is emptied (from the reader)
  Serial.flush();
}

void loop() {
  time = millis();
  Serial.print("Time="); 
  Serial.print(time);
  axisValue = analogRead(xAxis);
  Serial.print(",X=");
  Serial.print(axisValue); 
  axisValue = analogRead(yAxis);
  Serial.print(",Y=");
  Serial.print(axisValue);
  axisValue = analogRead(zAxis);
  Serial.print(",Z=");
  Serial.println(axisValue);
  
  // 5 times a second
  delay(30);
}
