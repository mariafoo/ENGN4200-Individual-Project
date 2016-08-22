int ledCount = 17;
int ledPins[] = {5,6,7,8,9,10,11,12,13,12,11,10,9,8,7,6,5};
int ledDelay = 100;
int buttonPin = 2;

void setup() {
  // activate all pins
  for (int thisLed = 0; thisLed < ledCount; thisLed++) {
    pinMode(ledPins[thisLed], OUTPUT);
  }
  pinMode(buttonPin, INPUT);
}

void loop() {
  // lights blinking forwards and then backwards
  for (int thisLed = 0; thisLed < ledCount-1; thisLed++) {
    digitalWrite(ledPins[thisLed], HIGH);
    delay(ledDelay);
    // activate response when button is pressed
    while(digitalRead(buttonPin) == HIGH) {
      //delay(100); // pause at light
      for (int thisLed = 0; thisLed < ledCount-1; thisLed++) {
        digitalWrite(ledPins[thisLed], HIGH);
        delay(10);
        digitalWrite(ledPins[thisLed], LOW); // blink faster
      //for (int thisLed = 0; thisLed < ledCount-1; thisLed++) {
        //digitalWrite(ledPins[thisLed], HIGH);
        //delay(10); // activate all lights
      }
    }
    digitalWrite(ledPins[thisLed], LOW); // continue with original blinking
  }
}
