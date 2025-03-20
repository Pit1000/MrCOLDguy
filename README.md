# Dr COLDguy

https://github.com/user-attachments/assets/7a6b5590-7840-4bb3-abfa-e16143a9db9b

#### Description: The created project included programming the ESP8266 microcontroller in the C language. The microcontroller's task is to read the temperature and humidity from the DHT22 digital sensor and then send it via WIFI using JSON to the server created in Flask. Flask server deals with saving data in a sqlite3 DB. By implementing the chart.js library, basic data visualization is achivable. Another implementation is DataTables (CSS, JS) which were used to present DB records in an accessible way with the possibility of filtering or sorting. The following libraries were used to program the microcontroller used in the project: DHT.h - which is responsible for handling the DHT-22 digital temperature and humidity sensor. ArduinoJson.h - which is responsible for handling the saving of the sensor data in JSON format preparing it for shipping. ESP8266WiFi.h - which is responsible for establishing a connection to a WiFi wireless network. ESP8266HTTPClient.h - which is responsible for sending and handling HTML requests to the server.
#### Flask/app.py:  Another important part of the project was a server made in the Flask framework programmed in python. The task of the server is to accept data from the microcontroller sent in JSON and store it in the DB. Then the individual server routes extract the information they need for visualization purposes. HTML, CSS, JS as well as the bootstrap library or DataTable were used to create the pages. The divison of the routes is as follows: Home Route (/): The main route requires user authentication and retrieves the latest temperature and humidity data from the database. Calculates the time difference between the current moment and the datetime stored in the database, and determines whether the data is considered "old." Depending on the result, it renders the "home.html" template with appropriate variables.. JSON Route (/json): Accepts JSON data through a POST request and inserts it into the database. History Route (/history): Displays the entire history of recorded temperature and humidity data. Plot Route (/plot): Displays a plot of temperature and humidity data based on user-selected sensor names. Sensors Route (/sensors): Provides information about available sensors, including sensor types, first recorded datetime, last recorded datetime, and the total count of records for each sensor. Logout Route (/logout): Clears the user's session, logging them out. Login Route (/login): Handles user login, checking credentials against the database. Scatterplot Route (/scatterplot): Displays a scatter plot of temperature and humidity data based on user-selected sensor names. Error Handling: An apology function is defined to render apology messages in case of errors.
#### Jinja2: Thanks to flask we have dynamic content rendering through various routes. used a very neat and clear way to create dynamic content with the help of templates and layouts that, depending on the required router, matched the router. Thanks to Jinja2, logic has been added to HTML5 to make use of it, for example for logging in and displaying alerts. 
#### DB sqlite3: In order to ensure good data management, it was decided to use a DB with the following tables and fields Table: temp This table appears to be used for storing temperature and humidity data. Fields: id: Primary key for the table, automatically incremented for each new record. sensor_type: Text field for storing the type of sensor. sensor_name: Text field for storing the name of the sensor. temperature: Real number field for storing temperature data. humidity: Real number field for storing humidity data. datetime: Text field for storing the date and time when the data was recorded. Table: users: This table is likely used for storing user authentication information. Fields: id: Primary key for the table, automatically incremented for each new user. username: Text field for storing the username of a user. hash: Text field for storing the hashed password of a user. The password is hashed for security reasons. An important part of the implementation is that by naming the sensors we distinguish them so theoretically you can connect many sensors to the server however this has not been tested yet. 
#### The following libraries were used to run the server on the flask framework. sqlite3: This module provides an interface to the SQLite database engine. It allows Python programs to interact with SQLite databases by executing SQL queries and managing connections. datetime: The datetime module supplies classes for working with dates and times. In this context, it's used for handling datetime-related operations, such as getting the current date and time. flash: The flash function in Flask is used to store a message that can be retrieved and rendered on the next request. It's often used for displaying notifications or feedback to users. jsonify: The jsonify function in Flask is used to create a JSON response from a Python dictionary or other data structures. It's commonly used in API routes to send JSON-formatted data. redirect: The redirect function in Flask is used to redirect the user to a different URL. It's often used after form submissions or other operations that require a redirection. render_template: The render_template function in Flask is used to render HTML templates. It allows embedding dynamic data into HTML files, making it easy to generate dynamic web pages. request: The request object in Flask provides access to incoming request data such as form data, query parameters, and more. It's used to retrieve data submitted by the user. session: The session object in Flask is a dictionary-like object that stores data across requests. It's often used for managing user sessions, storing user-specific information. Flask-Session: Flask-Session is a Flask extension that adds support for server-side session management. It allows storing session data on the server, providing additional security compared to client-side storage. functools: The functools module provides higher-order functions and operations on callable objects. In this context, it might be used for creating decorators. wraps: The wraps decorator from the functools module is used to transform a decorator function, preserving its signature and docstring. It's commonly used when creating custom decorators. werkzeug.security: Werkzeug is a utility library for Python. The werkzeug.security module provides tools for working with security-related tasks, such as hashing and checking passwords. In this context, it's used for password hashing and verification.         
