# IMPORTS
from supabase import Client
import questionary

class User:
    # Constructor
    def __init__(self, username = None, password = None):
        self.username = username
        self.password = password

    # Method to check password
    def check_password(self, password):
        return self.password == password
    
    # Method to change password
    def change_password(self, client: Client, new_password) -> bool:
        if new_password == self.password:
            print("New password cannot be the same as the old password.")
            return False
        else:
            self.password = new_password
            client.table("users").update({"password": self.password}).eq("username", self.username).execute()
            print("Password changed successfully!")
            return True
        
    # Method to login
    def login(self, supabase: Client) -> "User":
        while True:
            # user enters username, and the username is checked in the database
            username = questionary.text("Enter your username: ").ask()
            response = supabase.table("users").select("*").eq("username", username).execute()
            
            # if the username exists, the user enters the password, loops until the correct password is entered
            if response.data:
                while True:
                    password = questionary.password("Enter your password: ").ask()
                    user = response.data[0]
                    if user["password"] == password:
                        print("Logged in successfully!")
                        break
                    else:
                        print("Incorrect password!")
                        print("Please try again.")
                print("Welcome:", username)
                return User(username, password)

            # if the username does not exist, the user is prompted to try again
            else:
                print("Username does not exist!")
                print("Please try again.")
                return User()

    # Method to signup
    def signup(self, supabase: Client) -> "User":
        # loop to set username until a unique username is entered, and then the password is set
        while True:
            username = questionary.text("Choose your username: ").ask()
            user_name_is_taken = supabase.table("users").select("*").eq("username", username).execute()
            if user_name_is_taken.data:
                print("Username already exists!")
                print("Please choose another username.")
            else:
                password = questionary.password("Choose your password: ").ask()
                data = {"username": username, "password": password}
                response = supabase.table("users").insert(data).execute()
                if response:
                    print("Signed up successfully!")
                    print("Welcome:", username)
                    return User(username, password)
                else:
                    print("Error:", response)
                    return User()
        