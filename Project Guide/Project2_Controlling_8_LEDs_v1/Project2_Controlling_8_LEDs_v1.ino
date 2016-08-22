// Project Guide 
// Project 2: Controlling 8 LEDs
// Version 1

int ledCount = 9;
int ledPins[] = {5,6,7,8,9,10,11,12,13};
int ledDelay = 30;

void setup() {
  // activate all LED pins
  for (int thisLed = 0; thisLed < ledCount; thisLed++) {
    pinMode(ledPins[thisLed], OUTPUT);
  }
}

void loop() {
  // increments a counter to step forwards through the list
  for (int thisLed = 0; thisLed < ledCount; thisLed++) {
    digitalWrite(ledPins[thisLed], HIGH);
    delay(ledDelay);
    digitalWrite(ledPins[thisLed], LOW);
  }
  // starts at last position in the list and steps backwards
  for (int thisLed = ledCount-1; thisLed > 0; thisLed--) {
    digitalWrite(ledPins[thisLed], HIGH);
    delay(ledDelay);
    digitalWrite(ledPins[thisLed], LOW);
  }
}
