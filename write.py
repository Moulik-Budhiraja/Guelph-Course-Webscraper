import sqlite3
import json

# Path to your JSON file
json_file_path = 'courses.json'

# Path to your SQLite database
sqlite_file_path = 'courses.sqlite'

# Read the JSON file
with open(json_file_path, 'r') as file:
    courses = json.load(file)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(sqlite_file_path)
cursor = conn.cursor()

# Create a new table 'courses'
cursor.execute('''
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    offerings TEXT,
    prerequisites TEXT,
    coRequisites TEXT,
    equates TEXT,
    restrictions TEXT,
    department TEXT,
    locations TEXT
)
''')

# Insert courses into the table
for course in courses:
    cursor.execute('''
    INSERT INTO courses (title, description, offerings, prerequisites, coRequisites, equates, restrictions, department, locations) VALUES
    (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        course['title'],
        course['description'],
        course['offerings'],
        course['prerequisites'],
        course['coRequisites'],
        course['equates'],
        course['restrictions'],
        course['department'],
        course['locations']
    ))

# Commit changes and close connection
conn.commit()
conn.close()

print("Courses have been successfully inserted into the database.")
