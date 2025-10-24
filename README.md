# MrCOLDguy

---

> This project demonstrates the capabilities of IoT (Internet of Things), combining microcontrollers with web applications, for practical uses of both front-end and back-end technologies.

---

![MrCOLDguygif](https://github.com/user-attachments/assets/bd4db941-49f9-487b-bf76-91dc57ed4dac)

## PROJECT OVERVIEW 

A complete solution integrating an ESP8266 microcontroller with a Flask-based server.

1. **Data Collection:**  
   - The **ESP8266** microcontroller reads temperature and humidity from a **DHT22** sensor.

2. **Data Transmission:**  
   - Measurement data is sent in **JSON** format to the Flask server.

3. **Storage & Visualization:**  
   - The Flask application stores data in **SQLite3** and displays it via **chart.js** (for charts) and **DataTables** (for sortable and filterable tables).

## MOTIVATION

1. **Integration Demonstration**  
   Showcases the entire data flow – from sensor reading, through sending data to the server, to visual presentation.

2. **Education & Experimentation**  
   A practical example of combining hardware (sensor + microcontroller) with software (server, databases, front-end).

3. **Scalability Potential**  
   Thanks to the database configuration (including sensor names), the project can be expanded to handle multiple sensors and users (e.g., in smart home applications).

## IMPLEMENTATION

**Backend (Python/Flask):**
- **Python** – version 3.11 
- **Flask** – web framework  
- **Flask-Session** – server-side session management  
- **sqlite3** – database storing measurements and user info  
- **Additional Python libraries:**  
  - `datetime` – date and time operations  
  - `flash`, `jsonify`, `redirect`, `render_template`, `request`, `session` – Flask functions for notifications, JSON handling, redirects, templates, requests, and session handling  
  - `functools (wraps)` – decorators  
  - `werkzeug.security` – password hashing and verification

**Front-end & Data Visualization:**
- **HTML, CSS, JS** – essential building blocks of the user interface  
- **Bootstrap** – CSS framework for styling and responsiveness  
- **DataTables** – interactive tables with sorting and filtering  
- **chart.js** – charting library  
- **Jinja2** – template engine (Flask)

**Hardware & Microcontroller (C/C++):**
- **ESP8266** – microcontroller with built-in WiFi support  
- **DHT22** – temperature and humidity sensor  
- **DHT.h**, **ArduinoJson.h**, **ESP8266WiFi.h**, **ESP8266HTTPClient.h**










