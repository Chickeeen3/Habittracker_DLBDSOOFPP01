from database import *

"""In this file the analytic module is programed
    This includes:
    -return_all_habit_data 
    -return_habits_with_same_periodicity
    -show_logs
    -get_longest_streak_of_all
"""
def return_all_habits_data(connection):

    # returns all data of the currently stored habits

    habits_info = get_all_habit_data(connection)
    print(f"Currently {len(habits_info)} habits are being tracked:")
    print("\n")
    habits_list = []
    for habits in habits_info:
        print(f"Habit Name        : {habits[1]}")
        print(f"Period            : {habits[2]}")
        print(f"Date Created      : {habits[3]}")
        print(f"Streak            : {habits[4]}")
        print("\n")
        habits_list.append(habits)
    return habits_list

def show_logs(connection, habit_name):

    # Returns the log data of a specified habit

    result = get_log_data(connection, habit_name)
    return result


def return_habits_with_same_periodicity(connection, period):

    # returns habits with same chosen periodicity

    habits_info = get_habit_with_periodicity(connection, period)

    if len(habits_info) == 0:
        print(f"no '{period}' habits found")
    else:
        print(f"Your List of {period} habits are:")

    habit_names = []

    for habits in habits_info:
        print(f"{habits[1]}:")
        print(f"Date Created      : {habits[3]}")
        print(f"Current Streak    : {habits[4]}")
        print("\n")
        habit_names.append(habits[1])
    return habit_names


def get_longest_of_all(connection):

    # returns the longest streak of all habits,
    # print statement for the user, return for the test suit

    long = get_longest_streak(connection)
    print(f"Longest streak of all stored habits is \n {long} ")
    return long