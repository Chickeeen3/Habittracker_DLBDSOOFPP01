import sqlite3
from datetime import datetime
import datetime

"""In this file the creation and management of the database is programed
    This includes:
    -creation of the database
    -saving/retrieving data to/from database
    -deleting data
    -checking if a certain habit already exists in the database
    -adding predefined data of 5 habits
"""

def connect_db(name="main.db"):
    """
    establishing the connection to the sqlite3 database.
    :the database's title is main.db
    :creates a sqlite3 database and establishes a connection to it.
    """
    connection = sqlite3.connect(name)
    create_tables(connection)
    return connection

def create_tables(connection):
    #generates the tables Habit data & Habit_tracker
    c = connection.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS habits_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_name TEXT,
    period TEXT,
    created_at DATETIME,  
    streak INTEGER )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS habits_tracker (
    habit_name TEXT,
    period TEXT,
    current_streak INTEGER,
    checked_at DATETIME,
    FOREIGN KEY (habit_name) REFERENCES habits_data(habit_name),
    FOREIGN KEY (period) REFERENCES habits_data(period) )
    """)

    connection.commit()

def check_if_habit_exists(connection, habit_name):

    #checks to see if a specific habit is already stored in the database.
    c = connection.cursor()
    c.execute("SELECT habit_name FROM habits_data WHERE habit_name=?", (habit_name,))
    record = c.fetchall()
    if record:
        return True
    else:
        return False




def insert_habit_into_db(connection, habit_name, period, streak=0):
    """
    inserts a new habit into the database, if it does not already exist
    connection: used as a identifier with the sqlite database
    habit_name: The name of the habit
    period: The periodicy of the habit
    streak: The current streak of the habit, initially set to 0
    """
    c = connection.cursor()
    c.execute("SELECT habit_name FROM habits_data WHERE habit_name=?", (habit_name,))
    record = c.fetchone()
    if record:
        print("Habit already exists in database")
    else:
        date_created = datetime.date.today()
        c.execute("INSERT INTO habits_data VALUES (NULL,?,?,?,?)",
                  (str(habit_name), str(period), date_created, streak))
        c.execute("INSERT INTO habits_tracker VALUES (?,?,?,?)",
                  (str(habit_name), str(period), int(0), None))
        connection.commit()

def update_habit_tracker_streak(connection, habit_name, streak):
    """
    Saving the streak to habit_data set

    """
    c = connection.cursor()
    c.execute("UPDATE habits_data SET streak=? WHERE habit_name=?", (streak, habit_name))
    connection.commit()

def check_off_habit(connection, habit_name, period, current_streak, checked_at=None):

    # Saves the cheked_at date & current streak to the habit tracker.

    c = connection.cursor()
    c.execute("INSERT INTO habits_tracker VALUES(?,?,?,?)", (habit_name, period, current_streak, checked_at))
    connection.commit()

def erase_habit(connection, habit_name):

   # Erases the given habit+ tracking data from the database.

    c = connection.cursor()
    c.execute("DELETE FROM habits_data WHERE habit_name=?", (habit_name,))
    c.execute("DELETE FROM habits_tracker WHERE habit_name=?", (habit_name,))
    connection.commit()




def get_log_data(connection, habit_name):

    # retrieves all log data for a choosen habit

    c = connection.cursor()
    c.execute('SELECT checked_at FROM habits_tracker WHERE habit_name=?', (habit_name,))
    log = c.fetchall()
    print(f"Your logs for {habit_name}")
    print(f"checked at \n {log}")
    return log


def get_habit_with_periodicity(connection, period):
    # returns the habit with the same chosen periodicity
    c = connection.cursor()
    c.execute("SELECT * FROM habits_data WHERE period=?", (period,))
    return c.fetchall()

def get_all_habit_data(connection):

   # retrieves all habits attributes from database

    c = connection.cursor()
    c.execute("SELECT * FROM habits_data")
    return c.fetchall()

def get_habit_data(connection, habit_name, info):
    """
    retrieve the relevant habit information from relevant table
    info is either streak, periodicity or checked_at
    """
    c = connection.cursor()
    if info== "streak":
        c.execute("SELECT current_streak FROM habits_tracker WHERE habit_name=?", (habit_name,))
        streaks = c.fetchall()
        return streaks[-1][0]
    elif info== "periodicity":
        c.execute("SELECT period FROM habits_data WHERE habit_name=?", (habit_name,))
        return c.fetchall()[0][0]
    else:
        c.execute("SELECT checked_at FROM habits_tracker WHERE habit_name=?", [habit_name])
        return c.fetchall()[-1][0]


def get_longest_streak_of_habit(connection, habit_name):

    # returns the longest streak of specific habit

    c = connection.cursor()
    c.execute("SELECT streak FROM habits_data WHERE habit_name=?", (habit_name,))
    return c.fetchall()[0][0]

def get_longest_streak(connection):
    # returns the longest streak of all defined habits
    c = connection.cursor()
    c.execute(
        "SELECT DISTINCT habit_name,streak FROM habits_data WHERE streak=(SELECT MAX(streak) FROM habits_data)")
    return c.fetchall()

def add_predefined_habits(connection):
    predefined_habits = [
        ("Shower", "Daily"),
        ("Call_parents", "Weekly"),
        ("Learn_spanish",  "Daily"),
        ("Volunteer_at_shelter", "Weekly"),
        ("Floss", "Weekly")
    ]
    for habit in predefined_habits:
        if check_if_habit_exists(connection, habit[0]) is not True:
            insert_habit_into_db(connection, habit[0], habit[1])
            if habit[0]=="Shower":
                check_off_habit(connection, "Shower", "Daily", 1, "2024-01-14 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 1, "2024-01-17 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 2, "2024-01-18 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 3, "2024-01-19 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 4, "2024-01-20 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 1, "2024-02-01 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 2, "2024-02-02 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 3, "2024-02-03 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 4, "2024-02-04 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 5, "2024-02-05 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 6, "2024-02-06 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 7, "2024-02-07 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 8, "2024-02-08 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 9, "2024-02-09 00:00:00")
                check_off_habit(connection, "Shower", "Daily", 10, "2024-02-10 00:00:00")

            if habit[0] == "Call_parents":
                check_off_habit(connection, "Call_parents", "Weekly", 1, "2024-01-14 00:00:00")
                check_off_habit(connection, "Call_parents", "Weekly", 2, "2024-01-21 00:00:00")
                check_off_habit(connection, "Call_parents", "Weekly", 3, "2024-01-28 00:00:00")
                check_off_habit(connection, "Call_parents", "Weekly", 4, "2024-02-04 00:00:00")
                check_off_habit(connection, "Call_parents", "Weekly", 5, "2024-02-11 00:00:00")

            if habit[0] == "Learn_spanish":
                check_off_habit(connection, "Learn_spanish", "Daily", 1, "2024-01-17 00:00:00")
                check_off_habit(connection, "Learn_spanish", "Daily", 2, "2024-01-18 00:00:00")
                check_off_habit(connection, "Learn_spanish", "Daily", 3, "2024-01-19 00:00:00")
                check_off_habit(connection, "Learn_spanish", "Daily", 1, "2024-01-23 00:00:00")
                check_off_habit(connection, "Learn_spanish", "Daily", 2, "2024-01-24 00:00:00")
                check_off_habit(connection, "Learn_spanish", "Daily", 1, "2024-01-30 00:00:00")
                check_off_habit(connection, "Learn_spanish", "Daily", 2, "2024-01-31 00:00:00")
                check_off_habit(connection, "Learn_spanish", "Daily", 3, "2024-02-01 00:00:00")
                check_off_habit(connection, "Learn_spanish", "Daily", 4, "2024-02-02 00:00:00")
                check_off_habit(connection, "Learn_spanish", "Daily", 5, "2024-02-03 00:00:00")
                check_off_habit(connection, "Learn_spanish", "Daily", 6, "2024-02-04 00:00:00")
                check_off_habit(connection, "Learn_spanish", "Daily", 7, "2024-02-05 00:00:00")

            if habit[0] == "Volunteer_at_shelter":
                check_off_habit(connection, "Volunteer_at_shelter", "Weekly", 1, "2024-01-15 00:00:00")
                check_off_habit(connection, "Volunteer_at_shelter", "Weekly", 1, "2024-02-05 00:00:00")

            if habit[0] == "Floss":
                check_off_habit(connection, "Floss", "Weekly", 1, "2024-01-19 00:00:00")
                check_off_habit(connection, "Floss", "Weekly", 2, "2024-01-26 00:00:00")
                check_off_habit(connection, "Floss", "Weekly", 1, "2024-02-10 00:00:00")

                update_habit_tracker_streak(connection, "Shower", 10)
                update_habit_tracker_streak(connection, "Call_parents", 5)
                update_habit_tracker_streak(connection, "Learn_spanish", 7)
                update_habit_tracker_streak(connection, "Volunteer_at_shelter", 1)
                update_habit_tracker_streak(connection, "Floss", 1)

