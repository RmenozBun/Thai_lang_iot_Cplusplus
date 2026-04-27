#include <Arduino.h>

int led = 10;

void setup(){
    Serial.begin(9600);
    pinMode(led, OUTPUT);
    digitalWrite(led, LOW);
}

void loop(){
    digitalWrite(led, HIGH);
    delay(100);
    digitalWrite(led, LOW);
    delay(100);
}