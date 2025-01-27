# IMPORTS
import arrow
import questionary
from supabase import Client
import Classes.habit as h
from functions import general

class HabitEvent:

    # Constructor
    def __init__(self, habit_name='', date='', user=''):
        self.habit_name = habit_name
        self.date = date
        self.user = user

    # Method to add habit event
    def addHabitEvent(self, supabase: Client, user):
        habits = general.view_habits(supabase, user) 

        if habits != []:        
            habit_names = [habit.name for habit in habits]

            # option to select habit to add event to
            habit_name = questionary.select(
                "Select the habit you want to add an event to:",
                habit_names
            ).ask()

            # Check if habit event already exists for today (events should be added once per day at most)
            habit_events = supabase.table("habit_events").select("*").eq("habit_name", habit_name).order("date", desc=True).execute().data

            
            if any(event["date"] == arrow.now().format("YYYY-MM-DD") for event in habit_events):
                print("Habit already completed today!")
                return HabitEvent()

            # setting habit event object to be added to the database
            data = {"habit_name": habit_name, "date": arrow.now().format("YYYY-MM-DD"), "user": user.username}
            response = supabase.table("habit_events").insert(data).execute()
            habit_events.insert(0, response.data[0])

            # check if habit event was added successfully
            if response:
                print("Habit event added successfully!")
                        
                # update longest streak if habit was completed yesterday
                habit = next((h for h in habits if h.name == habit_name), None)
                habit.updateStreak(supabase, habit_events, False)
                return HabitEvent(habit_name, arrow.now(), user.username)
            else:
                print("Failed to add habit event!")
                print("Error:", response)
                return HabitEvent()
            
        else:
            return HabitEvent()
        