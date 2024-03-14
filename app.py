
import sqlite3
import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

DATABASE = '/workspaces/58105551/project/temp.db'

# Configure application
app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Ensure templates are auto-reloaded
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == 'GET':
        try:
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()

                select = cur.execute('''SELECT * FROM temp ORDER BY datetime DESC LIMIT 1''').fetchall()
                sensor_names = cur.execute('''SELECT *, MAX(datetime) FROM temp GROUP BY sensor_name''').fetchall()
                datetime_db = select[0][5]
                sellen = len(select)
                con.commit()
                msg = "Record successfully SELECTed"
                print(msg)
        except:
            con.rollback()
            msg = "error in SELECT operation on DB"
            print(msg)
            return apology(msg)

        finally:
            con.close()
            dt_now = datetime.now()
            dt_db = datetime.strptime(datetime_db, "%Y-%m-%d %H:%M:%S.%f")
            olddate = (dt_now - dt_db)
            if (olddate).total_seconds() >  500:
                return render_template("home.html", olddate=olddate, sensor_names=sensor_names)
            return render_template("home.html", sensor_names=sensor_names)

@app.route("/json", methods=["POST"])
def json():
    if request.method == 'POST':
        try:
            json_data = request.get_json()
            sensor_type = json_data["sensor_type"]
            sensor_name = json_data["sensor_name"]
            temperature = float(round(json_data["temperature"], 2))
            humidity = float(round(json_data["humidity"], 2))

            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO temp (sensor_type, sensor_name, temperature, humidity, datetime) VALUES(?, ?, ?, ?, ?)''', (sensor_type, sensor_name, temperature, humidity, datetime.now()))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"
            print(msg)
            return msg

        finally:
            con.close()
            return "Thanks for JSON"

@app.route("/history", methods=["GET"])
@login_required
def history():
    if request.method == 'GET':
        try:
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                select = cur.execute('''SELECT * FROM temp ORDER BY datetime DESC''').fetchall()
                con.commit()
                msg = "Record successfully SELECTed"
                print(msg)
        except:
            con.rollback()
            msg = "error in SELECT operation on DB"
            print(msg)
            return apology(msg)

        finally:
            con.close()
            return render_template("history.html", portfolio=select)

@app.route("/plot", methods=["GET", "POST"])
@login_required
def plot():
    if request.method == 'POST':
        try:
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                con.commit()
                sensor_name = request.form.get("sensor_name")
                sensic = cur.execute('''SELECT * FROM temp WHERE sensor_name = ? ORDER BY datetime ASC''',
                                     (sensor_name,)).fetchall()
        except:
            con.rollback()
            msg = "error in SELECT operation on DB"
            print(msg)
            return apology(msg)

        finally:
            con.close()
            temp_data = [row[5] for row in sensic]
            temp_data_objects = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f') for date_str in temp_data]
            formatted_temp_data = [date_obj.strftime('%H:%M %d-%m-%Y') for date_obj in temp_data_objects]
            temp_value = [row[3] for row in sensic]
            hum_value = [row[4] for row in sensic]
            return render_template("plot.html", temp_data=formatted_temp_data, temp_value=temp_value, hum_value=hum_value)
    else:
        try:
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                symbols = cur.execute('''SELECT * FROM temp GROUP BY sensor_name''').fetchall()
                con.commit()
                msg = "Record successfully SELECTed"
        except:
            con.rollback()
            msg = "error in SELECT operation on DB"
            print(msg)
            return apology(msg)

        finally:
            con.close()
            symbols = [row[2] for row in symbols]
            return render_template("plot_ch.html", symbols=symbols)



@app.route("/sensors", methods=["GET"])
@login_required
def sensors():
    if request.method == 'GET':
        try:
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                first = {}
                last = {}
                count = {}
                sensor_type = {}
                sensor_names = cur.execute(''' SELECT sensor_name FROM temp GROUP BY sensor_name ''').fetchall()
                for sensor_name in sensor_names:
                    sensor_type[sensor_name[0]] = cur.execute(
                        ''' SELECT sensor_type FROM temp WHERE sensor_name = ? GROUP BY sensor_name LIMIT 1''',
                        (sensor_name)).fetchall()
                    count[sensor_name[0]] = cur.execute(''' SELECT count(*) FROM temp WHERE sensor_name = ? GROUP BY sensor_name ''', (sensor_name)).fetchall()
                    first[sensor_name[0]] = cur.execute(''' SELECT datetime FROM temp WHERE sensor_name = ? ORDER BY datetime ASC LIMIT 1''', (sensor_name)).fetchall()
                    last[sensor_name[0]] = cur.execute(
                        ''' SELECT datetime FROM temp WHERE sensor_name = ? ORDER BY datetime DESC LIMIT 1''',
                        (sensor_name)).fetchall()
                con.commit()
                msg = "Record successfully SELECTed"
                print(msg)
        except:
            con.rollback()
            msg = "error in SELECT operation on DB"
            print(msg)
            return apology(msg)

        finally:
            con.close()
            sellen = len(sensor_names)
            return render_template("sensors.html", sensors=sensor_names, total=sellen, first=first, last=last, count=count, sensor_type=sensor_type)

@app.route("/logout", methods=["GET"])
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash('logged out!', 'primary')
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        try:
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                rows = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
                con.commit()
                msg = "Record successfully added"
                print(msg)
        except:
            con.rollback()
            msg = "error in insert operation"
            print(msg)
        finally:
            con.close()

        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0][0]

        flash('You logged in!', 'primary')
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/scatterplot", methods=["GET", "POST"])
@login_required
def scatterplot():
    if request.method == 'POST':
        try:
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                con.commit()
                sensor_name = request.form.get("sensor_name")
                sensic = cur.execute('''SELECT * FROM temp WHERE sensor_name = ? ORDER BY datetime ASC''',
                                     (sensor_name,)).fetchall()
        except:
            con.rollback()
            msg = "error in SELECT operation on DB"
            return apology(msg)

        finally:
            con.close()
            temp_value = [row[3] for row in sensic]
            hum_value = [row[4] for row in sensic]
            return render_template("scatterplot.html", temp_value=temp_value, hum_value=hum_value)
    else:
        try:
            with sqlite3.connect(DATABASE) as con:
                cur = con.cursor()
                symbols = cur.execute('''SELECT * FROM temp GROUP BY sensor_name''').fetchall()
                con.commit()
                msg = "Record successfully SELECTed"
                print(msg)
        except:
            con.rollback()
            msg = "error in SELECT operation on DB"
            print(msg)
            return apology(msg)

        finally:
            con.close()
            symbols = [row[2] for row in symbols]
            return render_template("scatterplot_ch.html", symbols=symbols)
