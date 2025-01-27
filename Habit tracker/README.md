# Project: Habit tracker

## Table of Contents
1. [General Info](#General-Info)
2. [Installation](#Installation)
3. [Usage and Main Functionalities](#Usage-and-Main-Functionalities)
4. [Contributing](#Contributing)


## General Info
This is a habit tracker to keep track of habits such as activities you choose to track, this program was made as a project for my university (B.Sc. Computer Science). In the app you are able to add habits, and later on add events of that abit to keep track of. There are also a number of ways of analysing those habits later on, such as comparing streaks of the habits, number of events and more.

## Installation

**Requirements:** 
Make sure you have Python 3.7+ installed on your computer. You can download the latest version of Python [here](https://www.python.org/downloads/). 

**How To:**<br>
1. Clone this repo to your machine 
```
git clone git@github.com:mksdznk/Habit-tracker.git
```

2.  Req. Package:
* arrow (install via ```pip install arrow```)
* supabase (install via ```pip install supabase```)
* questionary (install via ```pip install questionary```)

3. Run the program through the "main.py" file (press run python file from your IDE or navigate to project folder in terminal and type ```python main.py```)  and interact with the CLI

## Usage and Main Functionalities

#### 0. Register

* Possibility to create a user profile. 
* You are prompted to enter a username and password. 
* If the username is already taken, you are prompted for a new one. 
* If everything is filled out correctly, your profile is created and you are logged in to the program. 

---
#### 1. Login
* Enter your username and password to login. (if you already have an account, or use the account with pre-populated data: {username: user1, password: asdf})

---
#### 2. View / edit habits
A list of all your habits is shown where you can select a habit view / edit with the following functionalities:
* Edit habit
* Delete habit
* Total events
* Current streak
* Last event

---
#### 3. Create a Habit, or add an event to it 
* You are able to create your own habits.
* To do so, you are prompted for a habit name and its periodicity, and a description  
* To mark your progress, just select the habit you want to mark as completed. 

---
#### 4. Find habit by period
* Type in period and get a list of all habits with that periodicity
---
#### 5. Get longest streak
* Displays habit with the longest streak. 
          
#### 6. Change password

#### 7. Logout. 
