// Project Guide 
// Project 2: Controlling 8 LEDs
// Version 2

int ledCount = 17; 
int ledPins[] = {5,6,7,8,9,10,11,12,13,12,11,10,9,8,7,6,5};
int ledDelay = 100; 

void setup() {
  for (int thisLed = 0; thisLed < ledCount; thisLed++) {
    pinMode(ledPins[thisLed], OUTPUT);
  }
}

void loop() {
  for (int thisLed = 0; thisLed < ledCount-1; thisLed++) { 
    digitalWrite(ledPins[thisLed], HIGH);
    delay(ledDelay);
    digitalWrite(ledPins[thisLed], LOW);
  }

}
