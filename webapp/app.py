from flask import Flask, render_template, request
from pymysql import connections
import os

app = Flask(__name__)

# MySQL DB configuration
DBHOST = os.environ.get("DBHOST", "localhost")
DBUSER = os.environ.get("DBUSER", "root")
DBPWD = os.environ.get("DBPWD", "password")
DATABASE = os.environ.get("DATABASE", "employees")
DBPORT = int(os.environ.get("DBPORT", 3306))

# Custom group name and slogan from ConfigMap
GROUP_NAME = os.environ.get("GROUP_NAME", "CLO835 Team")
GROUP_SLOGAN = os.environ.get("GROUP_SLOGAN", "Building Reliable Cloud Apps")

# Background image URL from ConfigMap
BG_IMAGE = os.environ.get("BG_IMAGE", "/static/default.jpg")

# Print for logging
print(f"Using background image from: {BG_IMAGE}")

# Connect to MySQL
try:
    db_conn = connections.Connection(
        host=DBHOST,
        port=DBPORT,
        user=DBUSER,
        password=DBPWD,
        db=DATABASE
    )
except Exception as e:
    print("Database connection failed:", e)
    db_conn = None

# Routes
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', group_name=GROUP_NAME, group_slogan=GROUP_SLOGAN, bg_image=BG_IMAGE)

@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', group_name=GROUP_NAME, group_slogan=GROUP_SLOGAN, bg_image=BG_IMAGE)

@app.route("/addemp", methods=['POST'])
def AddEmp():
    if db_conn is None:
        return "Database connection failed"

    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"
    finally:
        cursor.close()

    return render_template('addempoutput.html', name=emp_name, group_name=GROUP_NAME, group_slogan=GROUP_SLOGAN, bg_image=BG_IMAGE)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", group_name=GROUP_NAME, group_slogan=GROUP_SLOGAN, bg_image=BG_IMAGE)

@app.route("/fetchdata", methods=['GET', 'POST'])
def FetchData():
    if db_conn is None:
        return "Database connection failed"

    emp_id = request.form['emp_id']
    output = {}

    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location FROM employee WHERE emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()
        if result:
            output["emp_id"] = result[0]
            output["first_name"] = result[1]
            output["last_name"] = result[2]
            output["primary_skills"] = result[3]
            output["location"] = result[4]
        else:
            return "Employee not found"
    except Exception as e:
        print(e)
        return "Error fetching data"
    finally:
        cursor.close()

    return render_template("getempoutput.html",
                           id=output["emp_id"],
                           fname=output["first_name"],
                           lname=output["last_name"],
                           interest=output["primary_skills"],
                           location=output["location"],
                           group_name=GROUP_NAME,
                           group_slogan=GROUP_SLOGAN,
                           bg_image=BG_IMAGE)

# Run app on port 81
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)

