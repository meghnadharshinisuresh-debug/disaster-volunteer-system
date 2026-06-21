import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Admins Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Admins (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Volunteers Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Volunteers (
    volunteer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    phone TEXT,
    skills TEXT
)
''')

# Help Requests Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Help_Requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    requester_name TEXT NOT NULL,
    location TEXT NOT NULL,
    request_type TEXT NOT NULL,
    contact_number TEXT,
    status TEXT DEFAULT 'Pending'
)
''')

# Relief Centers Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Relief_Centers (
    center_id INTEGER PRIMARY KEY AUTOINCREMENT,
    center_name TEXT NOT NULL,
    location TEXT NOT NULL,
    capacity INTEGER
)
''')

# Assignments Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    volunteer_id INTEGER,
    request_id INTEGER,
    FOREIGN KEY(volunteer_id) REFERENCES Volunteers(volunteer_id),
    FOREIGN KEY(request_id) REFERENCES Help_Requests(request_id)
)
''')

conn.commit()
conn.close()

print("Database Created Successfully")