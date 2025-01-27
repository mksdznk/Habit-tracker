# IMPORTS
import arrow
import questionary
from supabase import Client

class Habit:
    # Constructor
    def __init__(self, name='', description='', period=1, longest_streak=0, user=''):
        self.name = name
        self.description = description
        self.period = period
        self.longest_streak = longest_streak
        self.user = user
    
    # Method to add habit
    def addHabit(self, supabase: Client, user):
        habit_name = questionary.text("Enter the habit name: ").ask()
        
        # Check if habit already exists
        name_is_taken = supabase.table("habits").select("*").eq("name", habit_name).execute()
        if (name_is_taken.data):
            print("Habit already exists!")
            return Habit()
        
        # Get habit period, and make sure the entered value is an integer
        while True:
            habit_period = questionary.text("Enter the habit period (days): ").ask()
            try:
                habit_period = int(habit_period)
            except ValueError:
                print("Period must be an integer!")
                continue
            if (habit_period < 1):
                print("Period must be greater than 0!")
                continue

            # Get habit description
            habit_description = questionary.text("Enter the habit description: ").ask()
            
            # Setting habit object to be added to the database
            data = {
                "name": habit_name, 
                "period": habit_period, 
                "description": habit_description, 
                "user": user.username, 
                "longest_streak": 0
            }

            # Insert habit into the database and check if successful
            response = supabase.table("habits").insert(data).execute()
            if response:
                print("Habit added successfully!")
                return Habit(habit_name, habit_description, habit_period, 0, user.username)
            else:
                print("Failed to add habit!")
                print("Error:", response)
                return Habit()

    def deleteHabit(self, supabase: Client, habit_name: str):
        habit = supabase.table("habits").select("*").eq("name", habit_name).execute()
        if habit.data:
            response = supabase.table("habits").delete().eq("name", habit_name).execute()
            if response:
                print("Habit deleted successfully!")
            else:
                print("Failed to delete habit!")
                print("Error:", response)
        else:
            print("Habit not found!")

    def updateHabit(self, supabase: Client, user, old_habit_name):
        data = {
            "name": self.name,
            "period": self.period,
            "description": self.description,
        }
        response = supabase.table("habits").update(data).eq("name", old_habit_name).execute()
        if response:
            habit_events = supabase.table("habit_events").select("*").eq("user", user.username).eq("habit_name", self.name).order("date", desc=True).execute().data
            self.updateStreak(supabase, habit_events, True)
            print(response)
            print("Habit updated successfully!")
        else:
            print("Failed to update habit!")
            print("Error:", response)


    def updateStreak(self, supabase: Client, habit_events: list, new_period: bool):
        period = self.period
        counter = 1
        longest_streak = self.longest_streak
        longest_streak_to_update = 0

        if new_period:
            """
            Loop to update the longest streak of the habit
            
            If the parameter new_period is True, the longest streak is updated irregarless of the prevoius streak
            since a longer period may cause streak to be shorter than before
            """
            for i in range(len(habit_events)):
                if i == 0:
                    continue
                date1 = arrow.get(habit_events[i]["date"], "YYYY-MM-DD")
                date2 = arrow.get(habit_events[i - 1]["date"], "YYYY-MM-DD")
                dates_difference = (date2 - date1).days
                if dates_difference <= period:
                    counter += 1

                elif dates_difference > period:
                    if counter > longest_streak_to_update:
                        longest_streak_to_update = counter
                        counter = 1
            
                longest_streak = longest_streak_to_update if longest_streak_to_update > counter else counter

        elif not new_period:
            """
            loop to update the longest streak of the habit, only if the period is the same as before
            will only update the streak if it is larger than the previous streak
            """
            for i in range(len(habit_events)):
                if i == 0:
                    continue
                date1 = arrow.get(habit_events[i]["date"], "YYYY-MM-DD")
                date2 = arrow.get(habit_events[i - 1]["date"], "YYYY-MM-DD")
                dates_difference = (date2 - date1).days
                if dates_difference <= period:
                    counter += 1

                elif dates_difference > period:
                    if counter > longest_streak:
                        longest_streak_to_update = counter
                        counter = 1

        if (longest_streak_to_update > longest_streak) or (counter > longest_streak):
            longest_streak = longest_streak_to_update if longest_streak_to_update > counter else counter

        data = {
            "longest_streak": longest_streak
        }

        response = supabase.table("habits").update(data).eq("name", self.name).execute()

        if not response:
            print("Failed to update streak!")
            print("Error:", response)

    # Method to get total events
    def getTotalEvents(self, supabase: Client, user):
        habit_events = supabase.table("habit_events").select("*").eq("user", user.username).eq("habit_name", self.name).execute().data
        if habit_events:
            print("Total events:", len(habit_events))
        else:
            print("No events added yet!")
        
    # Method to get current streak
    def getCurrentStreak(self, supabase: Client, user):
        habit_events = supabase.table("habit_events").select("*").eq("user", user.username).eq("habit_name", self.name).order("date", desc=True).execute().data

        streak_counter = 1

        if habit_events:
            for i in range(len(habit_events) - 1):
                if i == 0:
                    continue
                date1 = arrow.get(habit_events[i]["date"], "YYYY-MM-DD")
                date2 = arrow.get(habit_events[i + 1]["date"], "YYYY-MM-DD")
                dates_difference = (date1 - date2).days
                if dates_difference <= self.period:
                    streak_counter += 1
                else:
                    break
            print("Current streak:", streak_counter)

        else:
            print("No events added yet!")

    # Method to get last event
    def getLastEvent(self, supabase: Client, user):
        habit_events = supabase.table("habit_events").select("*").eq("user", user.username).eq("habit_name", self.name).order("date", desc=True).execute().data
        
        if habit_events:
            print("Last event:", habit_events[0]["date"])
        else:
            print("No events added yet!")

