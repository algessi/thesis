from flask import Flask, render_template, request, jsonify
import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)

# Function to connect to the database
def connect_db():
    conn = sqlite3.connect("hospital.db")
    return conn

# Initialize the database and create resources table if not exists
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS resources (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        doctors_available INTEGER,
                        staff_available INTEGER,
                        beds_available INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# Home route to display the latest 7 records
@app.route("/")
def index():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM resources ORDER BY date DESC LIMIT 7", conn)
    conn.close()
    return render_template("index.html", data=df.to_dict(orient="records"))

# Route to add resources (POST request)
@app.route("/add", methods=["POST"])
def add_resource():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO resources (date, doctors_available, staff_available, beds_available) VALUES (?, ?, ?, ?)",
                   (data["date"], data["doctors"], data["staff"], data["beds"]))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 201

# Route for making predictions on the next day's resource needs (based on linear regression)
@app.route("/predict", methods=["GET"])
def predict():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM resources", conn)
    conn.close()
    
    if len(df) < 2:  # Need at least 2 rows for prediction
        return jsonify({"error": "Not enough data for prediction"}), 400
    
    # Prepare the data for linear regression
    X = np.array(range(len(df))).reshape(-1, 1)  # Sequence of days
    y = df["beds_available"]  # Beds availability as target variable
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict for the next day (next_day = number of existing records)
    next_day = len(X)
    prediction = model.predict([[next_day]])
    
    return jsonify({"predicted_beds": prediction[0]})

# New route for displaying predictions from the database
@app.route("/predictions")
def show_predictions():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()

    # Fetch predictions from the database
    cursor.execute("SELECT date, doctors_available, staff_available, beds_available FROM predictions")
    predictions = cursor.fetchall()
    conn.close()

    return render_template("predictions.html", predictions=predictions)

if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask
# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello, Flask is running!"

# if __name__ == "__main__":
#     app.run(debug=True)

