from Habit import Habit
from database import *
from Analytics import *
import os

"""In this file the test environment is programed
    This includes:
    -testing all class methods
    -testing all analytic functions
"""

class TestHabitTracker:

    db = None

    def setup_method(self):
        self.db = connect_db(name="test.db")
        add_predefined_habits(self.db)

    def test_all_habit_class_methods(self):

        # creating a daily and later a weekly Habit objects, testing all habit functions
        daily_habit = Habit(self.db,"Eat healty", "Daily")
        daily_habit.save_habit(self.db)
        # test if habit is created
        assert check_if_habit_exists(self.db, "Eat healty") is not False

        # tests tracking works as intended
        daily_habit.track_habit(self.db)
        # tracking should fail as habit has already been checked
        daily_habit.track_habit(self.db)

        # if both tests above go as planned, streak should be one
        assert get_habit_data(self.db, "Eat healty", "streak") == 1

        # same test for a weekly habit as for the daily habit
        weekly_habit = Habit(self.db, "Reconnect with old friends", "Weekly")
        weekly_habit.save_habit(self.db)
        assert check_if_habit_exists(self.db, "Reconnect with old friends")

        weekly_habit.track_habit(self.db)
        weekly_habit.track_habit(self.db)

        assert get_habit_data(self.db, "Reconnect with old friends", "streak") == 1

        # test delete habit
        daily_habit.delete_habit(self.db)
        assert check_if_habit_exists(self.db, "Eat healty") is False

        weekly_habit.delete_habit(self.db)
        assert check_if_habit_exists(self.db, "Reconnect with old friends") is False


    def test_all_analytics_functions(self):
        # The number of predefined habits should be 5
        all_habits = return_all_habits_data(self.db)
        assert len(all_habits) == 5

        # call parents was tracked 5 times, with the initial saved at date, log data contain 6 entries
        log_data = show_logs(self.db, "Call_parents")
        assert len(log_data) == 6

        # get daily habits should result in "shower" & "learn spanish"
        daily_habits = return_habits_with_same_periodicity(self.db, "Daily")
        daily_predefined = ["Shower", "Learn_spanish"]
        assert set(daily_habits) == set(daily_predefined)

        # get weekly habits should result in "call parents", "volunteer at shelter" & "Floss"
        weekly_habits = return_habits_with_same_periodicity(self.db, "Weekly")
        weekly_predefined = ["Call_parents", "Volunteer_at_shelter", "Floss"]
        assert set(weekly_habits) == set(weekly_predefined)

        # the longest streak of all habits should be 10 (shower)
        longest_streak_of_all_habits = get_longest_of_all(self.db)
        assert longest_streak_of_all_habits[0][1] == 10

        # the longest streak of "Learn spanish" should be 7
        longest_streak_of_habit = get_longest_streak_of_habit(self.db, "Learn_spanish")
        assert longest_streak_of_habit == 7


    def teardown_method(self):
        self.db.close()
        os.remove("test.db")