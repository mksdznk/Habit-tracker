from supabase import Client
from Classes.habit import Habit

# Method to view habits
def view_habits(supabase: Client, user) -> list[Habit]:
    habits = supabase.table("habits").select("*").eq("user", user.username).execute()
    habits_to_return = []
    if habits.data != []:
        for habit in habits.data:
            habits_to_return.append(Habit(habit["name"], habit["description"], habit["period"], habit["longest_streak"], habit["user"]))
        return habits_to_return
    else:
        print("No habits added yet!")
        return []

def view_habits_with_periodicity(supabase: Client, user, period: int) -> list[Habit]:
    habits = supabase.table("habits").select("*").eq("user", user.username).eq("period", period).execute()
    if len(habits.data) != 0:
        print("Habits with periodicity of ", period, " days:")
        for habit in habits.data:
            print("Habit name: ", habit["name"])
    else:
        print("No habits with that periodicity!")

def overall_longest_streak(supabase: Client, user):
    habits = supabase.table("habits").select("*").eq("user", user.username).order("longest_streak", desc=True).execute()
    if len(habits.data) != 0:
        print("Overall longest streak: ", habits.data[0]["longest_streak"], ", on habit: ", habits.data[0]["name"])
    else:
        print("No habits added yet!")