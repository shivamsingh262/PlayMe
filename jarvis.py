import sqlite3
import subprocess
import re
designation = {"M":"sir","F":"mam"}
sex = ""
name = ""
special_commands = ['play movie']
connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()

def greeting():
    global name
    name = raw_input("Who are you? ")
    if user_exists(name) == False:
        global sex
        sex = raw_input("Are you a guy? ")
        if "no" in sex:
            sex = "F"
        else:
            sex = "M"
        add_user(name,sex)
    else:
        sex = male_female(name)
    take = raw_input("Hello " + designation[globals()['sex']] + " how are you? ")
    print sense_greeting(take)
    conversation()
    raw_input("Waiting...")

def add_user(name,sex):
    cursor.execute("INSERT INTO user(name,sex) VALUES (?,?)",(name,sex))
    connection.commit()

def user_exists(name):
    statement = "SELECT name,sex FROM user WHERE name = (?)"
    cursor.execute(statement,(name,))
    id = cursor.fetchall()
    if id:
        return True
    else:
        return False
    
def male_female(name):
    statement = "SELECT sex FROM user WHERE name = (?)"
    cursor.execute(statement,(name,))
    id = cursor.fetchall()
    return id[0][0]

def sense_greeting(take):
    if ("you?" or "you ?") in take:
        return "I am fine " + globals()['name'] + ", thanks..."
    else:
        return "Okay..."

def conversation():
    question = raw_input("Let's talk " + globals()['name']+ ", type bye to well, you know ")
    while "bye" not in question:
        if question not in special_commands:
            answer = analyze(question)
            question = raw_input(answer+" ")
        else:
            process_special(question)
            question = raw_input("Playing now... ")
    else:
        print "Good bye " + designation[globals()['sex']] + ", nice talking to you"

def process_special(question):
    if 'movie' in question:
        param = 'movie'
    else:
        pass
    video = raw_input("Which "+param+" ? ")
    find_play(video.lower())

def analyze(question):
    #return "Garbage for now "
    ans = check_response(question)
    if ans == None:
        answer = raw_input("Please provide answer for this: ")
        add_response(question,answer)
        return "I will remember now, please continue "
    else:
        return ans

def check_response(question):
    statement = "SELECT answer FROM response WHERE question LIKE (?)"
    cursor.execute(statement,(('%'+question+'%'),))
    id = cursor.fetchall()
    if id:
        return id[0][0]
    else:
        return None

def add_response(question,answer):
    cursor.execute("INSERT INTO response(question,answer,added_by) VALUES (?,?,?)",(question,answer,globals()['name']))
    connection.commit()

def play_movie(url):
    subprocess.Popen([r"C:/Program Files (x86)/VideoLAN/VLC/vlc.exe",url.encode('unicode-escape')])

def find_play(name):
    cursor.execute("SELECT url FROM movies where name LIKE (?)",(('%'+name+'%'),))
    id = cursor.fetchall()
    if id:
        play_movie(id[0][0])
    else:
        print "Movie not found"

greeting()

