import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

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

cursor.execute('''
CREATE TABLE IF NOT EXISTS Assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    volunteer_id INTEGER,
    request_id INTEGER,
    assignment_status TEXT DEFAULT 'Assigned'
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Relief_Centers (
    center_id INTEGER PRIMARY KEY AUTOINCREMENT,
    center_name TEXT,
    address TEXT,
    contact_number TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Admins (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

conn.commit()
conn.close()

print("Database created successfully!")