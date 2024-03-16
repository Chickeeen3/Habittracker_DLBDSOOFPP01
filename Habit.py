from database import *
from datetime import *

"""In this file the definition and class methods of the habit class is programed
    This includes:
    -save/ delete habit
    -track habit
    -overwriting the longest streak in habit_data table
"""

class Habit:
    def __init__(self, connection, name: str, period):
        """Definition of the habit class, creation of a new object
            name: Name of the habit.
            period: A time-period for your habit (daily or weekly)
        """
        self.connection = connection
        self.name = name
        self.period = period
        self.streak = 0
        self.created_at = datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        return f"{self.name}:{self.period}"

    def save_habit(self, connection):
        # saves a habit to the database
        insert_habit_into_db(self.connection, self.name, self.period)

    def delete_habit(self, connection):
        # erases the habit from the database
        erase_habit(self.connection, self.name)
        self.name = None
        self.period = None
        self.streak = 0


    def check_event(self, evaluation):
        """increase the streak by 1 or resets counter to 1
        saves checked at date to database
        """
        if evaluation == "Success":
            self.streak+=1
        else:
            self.streak = 1
        check_off_habit(self.connection, self.name, self.period, self.streak, datetime.now().strftime("%Y-%m-%d"))
        self.longest(self.connection)

    def track_habit(self, connection):
        """tracks  the habit in the database"""

        streak = get_habit_data(self.connection, self.name, "streak")
        period = get_habit_data(self.connection, self.name, "periodicity")
        latest_check=get_habit_data(self.connection, self.name, "checked at")
        if not latest_check:
            latest_check=0
        else:
            latest_check = latest_check
        today = datetime.now().strftime("%Y-%m-%d")
        if period == 'Daily':
            if streak==0:
                # habit has yet to be checked
                self.check_event("Success")
                print("Habit checked succesfully")
            elif (datetime.strptime(today,"%Y-%m-%d")-datetime.strptime(latest_check,"%Y-%m-%d %H:%M:%S")).days< 1:
                # habit has already been checked today
                print("Habit Already Checked")
            elif (datetime.strptime(today,"%Y-%m-%d")-datetime.strptime(latest_check,"%Y-%m-%d %H:%M:%S")).days< 2:
                # habit was checked yesterday but not yet today
                self.check_event("Success")
                print("Habit checked succesfully")
            else:
                self.check_event("Failed")
                # habit hasn't checked yesterday, thus streak is reseted to 1
                print("Habit checked but streak is broken")

        else:
            today_datetime= datetime.strptime(today, "%Y-%m-%d")
            start_of_week=today_datetime-timedelta(days=today_datetime.weekday())
            #a=(datetime.strptime(latest_check,"%Y-%m-%d")-start_of_week).days
            if streak==0:
                # habit has yet to be checked
                self.check_event("Success")
                print("Habit checked succesfully")
            elif (datetime.strptime(latest_check,"%Y-%m-%d %H:%M:%S")-start_of_week).days< -7:
                # habit hasn't been checked last week, thus streak is reseted to 1
                self.check_event("Failed")
                print("Habit checked but streak is broken")
            elif (datetime.strptime(latest_check,"%Y-%m-%d %H:%M:%S")-start_of_week).days<= -1:
                # habit was checked last week but not yet this week
                self.check_event("Success")
                print("Habit checked succesfully")
            else:
                # habit has already been checked this week
                print("Habit Already Checked")




    def longest(self, connection):
    # saves a new longest streak to habit_data if current_streak> streak in habit data
        streak = get_habit_data(self.connection, self.name, "streak")
        longest_streak = get_longest_streak_of_habit(self.connection, self.name)
        if streak > longest_streak:
            update_habit_tracker_streak(self.connection, self.name, streak)
