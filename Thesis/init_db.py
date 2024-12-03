import sqlite3

# Initialize the database and insert the required data
def init_db():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    
    # Create the `resources` table with specified columns
    c.execute('''CREATE TABLE IF NOT EXISTS resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    doctors_available INTEGER NOT NULL,
                    staff_available INTEGER NOT NULL,
                    beds_available INTEGER NOT NULL)''')
    
    # Create the `predictions` table with specified columns
    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    doctors_available INTEGER NOT NULL,
                    staff_available INTEGER NOT NULL,
                    beds_available INTEGER NOT NULL)''')
    
    # Clear any existing data in the resources table (but leave predictions table data intact)
    c.execute("DELETE FROM resources")
    
    # Insert required data into resources table
    data = [
        ('2024-12-01', 10, 50, 20),
        ('2024-12-02', 8, 45, 18),
        ('2024-12-03', 12, 60, 25),
        ('2024-12-04', 9, 48, 22),
        ('2024-12-05', 11, 55, 23)
    ]
    c.executemany('''INSERT INTO resources (date, doctors_available, staff_available, beds_available)
                      VALUES (?, ?, ?, ?)''', data)
    
    conn.commit()
    conn.close()
    print("Database and data initialized successfully.")

if __name__ == '__main__':
    init_db()
