import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Historical data
data = {
    "date": ["2023-11-01", "2023-11-02", "2023-11-03", "2023-11-04", "2023-11-05"],
    "patient_count": [100, 120, 130, 90, 110],
    "doctors_available": [10, 12, 14, 9, 11],
    "staff_available": [20, 22, 25, 18, 21],
    "beds_available": [50, 45, 40, 55, 48],
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Preprocessing
df["date"] = pd.to_datetime(df["date"])
df["date_num"] = df["date"].map(pd.Timestamp.toordinal)

X = df[["date_num", "patient_count"]]
y = df[["doctors_available", "staff_available", "beds_available"]]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Generate future predictions
future_dates = pd.DataFrame({
    "date": pd.date_range("2023-11-06", "2023-11-10"),
    "patient_count": [115, 125, 140, 100, 120],
})
future_dates["date_num"] = future_dates["date"].map(pd.Timestamp.toordinal)

future_predictions = model.predict(future_dates[["date_num", "patient_count"]])
future_dates[["doctors_available", "staff_available", "beds_available"]] = future_predictions.round().astype(int)

# Save predictions to SQLite database
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

for _, row in future_dates.iterrows():
    cursor.execute("""
        INSERT INTO predictions (date, doctors_available, staff_available, beds_available)
        VALUES (?, ?, ?, ?)
    """, (row["date"].strftime("%Y-%m-%d"), row["doctors_available"], row["staff_available"], row["beds_available"]))

conn.commit()
conn.close()

print("Predictions saved to database successfully!")
