import click
from Analytics import *
from Habit import Habit

"""
In this file the main menu is created as a CLI    
"""
def main():
    """
    The main menu contains the functions of the app and the available submenus.
    The user is prompted to enter the required information via the command line.
    """
    connection = connect_db()
    add_predefined_habits(connection)
    print('Welcome to the habits tracker!')
    print('Choose one of the following options:')
    print('1. Create a new habit')
    print('2. Check habit')
    print('3. Delete habit')
    print('4. Analyse habits')
    print('5. Exit')


    choice = click.prompt("Enter your number of choice", type=int)
    connection = connect_db()
    # Creating a new habit & saving it to the database
    if choice == 1:
        connection = connect_db()
        print('Enter your new habit')
        habit_name = click.prompt("Name of Habit", type=str)
        if check_if_habit_exists(connection, habit_name):
            print("Habit already exists!")
            main()
        else:
            possible_periodicities = ["Daily", "Weekly"]
            periodicity = input("Enter the periodicity of the new habit (Daily, Weekly):").title()
            while periodicity not in possible_periodicities:
                print("Invalid periodicity")
                periodicity = input("Enter the new periodicity of the new habit (Daily, Weekly):").title()
            habit = Habit(connection, habit_name, periodicity)
            habit.save_habit(connection)
            print("Habit created successfully")
            main()



    # Checking a habit.
    elif choice == 2:
        connection = connect_db()
        Habit_name = click.prompt("Name of Habit", type=str)
        if check_if_habit_exists(connection, Habit_name):
            test=Habit(connection, Habit_name, "Null")
            test.track_habit(connection)
            main()
        else:
            print("Habit does not exist!")
            main()

# Deleting a habit from teh database
    elif choice == 3:
        connection = connect_db()
        Habit_name = click.prompt("Name of Habit", type=str)
        if check_if_habit_exists(connection, Habit_name):
            test = Habit(connection, Habit_name, "Null")
            test.delete_habit(connection)
            print("Habit " + Habit_name + " has been deleted!")
            main()
        else:
            print("Habit does not exist!")
        main()

# opening the analytic submenu
    elif choice == 4:
        print("Choose one of the following options:")
        print("1. Show all habits")
        print("2. Show all habits with periodicity")
        print("3. Show logs of one habit")
        print("4. Show a habit's streak")
        print("5. Show habit with the longest streak")
        print("6. Home")

        choice3 = click.prompt("Enter your choice", type=int)


        # Showing all habits stored in the App
        if choice3 == 1:
            return return_all_habits_data(connection)
            main()

        # Showing all habits stored in the App with a chosen periodicity
        elif choice3 == 2:
            possible_periodicities = ["Daily", "Weekly"]
            periodicity = input("Enter the new periodicity (Daily, Weekly):").title()
            while periodicity not in possible_periodicities:
                print("Invalid periodicity")
                periodicity = input("Enter the periodicity (Daily, Weekly):").title()
            return return_habits_with_same_periodicity(connection, periodicity)
            main()


        # Showing all logs of a specified habit
        elif choice3 == 3:
            Habit_name = click.prompt("Name of Habit", type=str)
            show_logs(connection, Habit_name)
            main()


        # Showing the current streak of a habit
        elif choice3 == 4:
            Habit_name = str(input("Name of the Habit: ")).title()
            streak_habit = get_habit_data(connection, Habit_name, "streak")
            print(streak_habit)
            main()

        # Showing the habit with the longest streak stored in the database
        elif choice3 == 5:
            long_streak = get_longest_of_all(connection)
            main()

        main()

    # Exiting the program
    else:
        print("Goodbye!")
        exit()


# If the user enters a number that is not in the menu, the program will remain in the main menu
if __name__ == "__main__":
    main()
