import sqlite3

conn = sqlite3.connect('prm_poc_tmp.db')  # Establish a connection to the SQLite database
cursor = conn.cursor() # Create a cursor object to execute SQL commands

# Creating the people table if it doesn't exist
try:
    cursor.execute('''CREATE TABLE people(
        person_id INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname TEXT,
        lastname TEXT,
        deceased BOOLEAN, -- dead persons should have 1
        works_at TEXT,
        job_title TEXT,
        date_of_birth DATE,
        last_contact DATE,
        last_IRL_hangout DATE,
        parent_of_id INTEGER, -- insert PRIMARY KEY of this persons child
        child_of_id INTEGER  -- insert PRIMARY KEY of this persons parent
        )''')
except sqlite3.OperationalError:
    print("Table people already exists")

try:
    cursor.execute("INSERT INTO people (firstname, person_id) VALUES (?,?)", ('Me', 1000))

except:
    pass

try:
    cursor.execute(
        '''CREATE TABLE activities (
        activity_id INTEGER PRIMARY KEY,
        activity_date DATE,
        activity_note TEXT
        )''')
except sqlite3.OperationalError:
    print("Table activities already exists")

try:
    cursor.execute('''
        CREATE TABLE junction_people_activities (
            participation_id INTEGER PRIMARY KEY,
            person_id INTEGER,
            activity_id INTEGER,
            FOREIGN KEY (person_id) REFERENCES people(person_id),
            FOREIGN KEY (activity_id) REFERENCES activities(activity_id)
        )
    ''')
except sqlite3.OperationalError:
    print("Table junction_people_activities already exists")


# 🟨 Dummy people
cursor.execute("INSERT INTO people (firstname, lastname) VALUES (?, ?)", ('Steve', 'Jobs'))
cursor.execute("INSERT INTO people (firstname, lastname) VALUES (?, ?)", ('Mark', 'Jason'))
cursor.execute("INSERT INTO people (firstname, lastname) VALUES (?, ?)", ('Jane', 'Smith'))
cursor.execute("INSERT INTO people (firstname, lastname) VALUES (?, ?)", ('Alice', 'Johnson'))


# 🟨 Dummy activities
cursor.execute("INSERT INTO activities (activity_date, activity_note) VALUES (?, ?)",
               ('2023-12-01', 'Coffee'))
cursor.execute("INSERT INTO activities (activity_date, activity_note) VALUES (?, ?)",
               ('2023-12-05', 'Training'))
cursor.execute("INSERT INTO activities (activity_date, activity_note) VALUES (?, ?)",
               ('2023-12-10', 'Lunch'))

# 🟨 Dummy people_in_activities
cursor.execute("INSERT INTO junction_people_activities (person_id, activity_id) VALUES (?,?)", (1000, 1))
cursor.execute("INSERT INTO junction_people_activities (person_id, activity_id) VALUES (?,?)", (1002, 1))
cursor.execute("INSERT INTO junction_people_activities (person_id, activity_id) VALUES (?,?)", (1000, 2))
cursor.execute("INSERT INTO junction_people_activities (person_id, activity_id) VALUES (?,?)", (1000, 3))
cursor.execute("INSERT INTO junction_people_activities (person_id, activity_id) VALUES (?,?)", (1001, 3))
cursor.execute("INSERT INTO junction_people_activities (person_id, activity_id) VALUES (?,?)", (1002, 3))


# Commit the changes and close the connection
conn.commit()
conn.close()

while True:
    userinput = input("choose a table to query: 1. people 2. activities 3. junction_people_activities: ")

    if userinput == "1":
        query = "SELECT * FROM people"
    elif userinput == "2":
        query = "SELECT * FROM activities"
    elif userinput == "3":
        query = "SELECT * FROM junction_people_activities"
    else:
        exit

    conn = sqlite3.connect('tmp_prm.db')  # Establish a connection to the SQLite database
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands

    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
