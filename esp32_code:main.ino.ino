#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11
#define SOIL_PIN 34
#define RELAY_PIN 26

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(RELAY_PIN, OUTPUT);

  digitalWrite(RELAY_PIN, HIGH); // OFF initially
}

void loop() {

  // 🔹 Read sensors
  int soilValue = analogRead(SOIL_PIN);
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // 🔹 Send to Python
  Serial.print(temperature);
  Serial.print(",");
  Serial.print(humidity);
  Serial.print(",");
  Serial.println(soilValue);

  // 🔹 Receive command from Python
  if (Serial.available()) {
    char cmd = Serial.read();

    if (cmd == '1') {
      digitalWrite(RELAY_PIN, LOW);   // ON
    }
    else if (cmd == '0') {
      digitalWrite(RELAY_PIN, HIGH);  // OFF
    }
  }

  delay(2000);
}