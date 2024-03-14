
#include "DHT.h"
#include <ArduinoJson.h>
#include <ArduinoJson.hpp>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define DHTPIN 4     // Digital pin  #2 on ESP8266
#define DHTTYPE DHT22 // Sensor type
DHT dht(DHTPIN, DHTTYPE);
float humidity, temperature_C;

/* this can be run with an emulated server on host:
        cd esp8266-core-root-dir
        cd tests/host
        make ../../libraries/ESP8266WebServer/examples/PostServer/PostServer
        bin/PostServer/PostServer
   then put your PC's IP address in SERVER_IP below, port 9080 (instead of default 80):
*/
//#define SERVER_IP "10.0.1.7:9080" // PC address with emulation on host
#define SERVER_IP "10.0.1.7:9080"

#ifndef STASSID
#define STASSID "--your_ssid--"
#define STAPSK "--your_password"
#endif

void setup() {

  Serial.begin(9600);

  Serial.println();
  Serial.println();
  Serial.println();

  WiFi.begin(STASSID, STAPSK);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());

  dht.begin();
}



void loop() {
  // wait for WiFi connection
  if ((WiFi.status() == WL_CONNECTED)) {

    WiFiClient client;
    HTTPClient http;

    // odczyt jeżeli Wifi.status ok
    temperature_C = dht.readTemperature();
    humidity = dht.readHumidity();

    // Check for error reading
    if (isnan(humidity) || isnan(temperature_C)) {
      Serial.println(" DHT reading failed ");
      return;
    }

    DynamicJsonDocument doc(300);
    doc["sensor_type"] = "DHT22";
    doc["sensor_name"] = "Kitchen";
    doc["temperature"] = temperature_C;
    doc["humidity"] = humidity;

    String postmessage;
    Serial.println(" ");
    serializeJson(doc, postmessage);
    Serial.println(" ");
    int len = measureJson(doc);

    Serial.print("[HTTP] begin...\n");
    // configure traged server and url
    http.begin(client, "http://" SERVER_IP "/json");  // HTTP
    http.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] POST...\n");
    // start connection and send HTTP header and body
    int httpCode = http.POST(postmessage);


    // httpCode will be negative on error
    if (httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] POST... code: %d\n", httpCode);

      // file found at server
      if (httpCode == HTTP_CODE_OK) {
        const String& payload = http.getString();
        Serial.println("received payload:\n<<");
        Serial.println(payload);
        Serial.println(">>");
      }
    } else {
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  }

  delay(60000);
}
