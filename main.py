# Library imports
import os
import questionary
from dotenv import load_dotenv
from supabase import create_client, Client

#Local imports
import Classes.habit as Habit
import Classes.habitEvent as HabitEvent
import Classes.user as User
from functions import general

# Load environment variables from .env
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Main function 
if __name__ == "__main__":
    user: User = User.User()

    # option to login or signup
    login_or_signup = questionary.select(
        "Do you want to login or signup?", 
        choices=["Login", "Signup"]
    ).ask()
    if login_or_signup == "Login":
        user = user.login(supabase)
    elif login_or_signup == "Signup":
        user = user.signup(supabase)

    # main menu for chosing what to do
    while True:
        main_menu_action = questionary.select(
            "What do you want to do?", 
            choices=["View / edit habits", "Add habit or habit event", "Find habit by period", "Get longest streak", "Change password", "Logout"]
        ).ask()

        # habits menu option
        if main_menu_action == "View / edit habits":
            #
            habits = general.view_habits(supabase, user)
            if habits != []:
                while True:
                    habit_names = [habit.name for habit in habits]

                    # option to select habit
                    habit_name = questionary.select(
                        "Select habit:",
                        habit_names
                    ).ask()

                    # get habit object
                    habit = next((h for h in habits if h.name == habit_name), None)

                    print("Habit name:" + habit.name)
                    print("Habit description:" + str(habit.description))
                    print("Habit period:" + str(habit.period))
                    print("Habit longest streak:" + str(habit.longest_streak))

                    habit_action = questionary.select(
                        "What do you want to do?", 
                        choices=["Edit habit", "Delete habit", "Total events", "Current streak", "Last event"]
                    ).ask()

                    if habit_action == "Edit habit":
                        old_habit_name = habit.name
                        habit_name = questionary.text("Enter new habit name: (press ENTER to keep the same)").ask()
                        habit_period = questionary.text("Enter new habit period (days): (press ENTER to keep the same)").ask()
                        habit_description = questionary.text("Enter new habit description: (press ENTER to keep the same)").ask()
                        
                        if habit_name.strip():
                            habit.name = habit_name
                        if habit_period.strip():
                            try:
                                habit.period = int(habit_period)
                            except ValueError:
                                print("Period must be an integer! Old value will be kept.")
                            except habit.period < 0:
                                print("Period")
                        if habit_description.strip():
                            habit.description = habit_description

                        habit.updateHabit(supabase, user, old_habit_name)
                        break

                    elif habit_action == "Delete habit":
                        habit.deleteHabit(supabase, habit.name)
                        break

                    elif habit_action == "Total events":    
                        habit.getTotalEvents(supabase, user)
                        break

                    elif habit_action == "Current streak":
                        habit.getCurrentStreak(supabase, user)
                        break

                    elif habit_action == "Last event":
                        habit.getLastEvent(supabase, user)
                        break

        # add habit / events option
        elif main_menu_action == "Add habit or habit event":
            while True:
                add_action = questionary.select(
                    "What do you want to do?", 
                    choices=["Add habit", "Add habit event"]
                ).ask()


                if add_action == "Add habit":
                    habit = Habit.Habit()
                    habit.addHabit(supabase, user)
                    break
                elif add_action == "Add habit event":
                    habit_event = HabitEvent.HabitEvent()
                    habit_event.addHabitEvent(supabase, user)
                    break

        # find habit by period option
        elif main_menu_action == "Find habit by period":                
            while True:
                habit_period = questionary.text("Enter new habit period (days): ").ask()
                if habit_period.strip(): 
                    try:
                        habit_period = int(habit_period)
                        break
                    except ValueError:
                        print("Period must be an integer!")
                        continue
            
            habits = general.view_habits_with_periodicity(supabase, user, habit_period)            

        # get longest streak option
        elif main_menu_action == "Get longest streak":
            general.overall_longest_streak(supabase,user)

        # change password option
        elif main_menu_action == "Change password":
            while True:
                old_password = questionary.password("Enter your old password: ").ask()
                if user.check_password(old_password):
                    while True:
                        new_password = questionary.password("Enter your new password: ").ask()
                        if user.change_password(supabase, new_password):
                            break        
                    break
                else:
                    print("Incorrect password!")
                    print("Please try again.")
                        
        # logout option
        elif main_menu_action == "Logout":
            print("Successfully logged out!")
            break