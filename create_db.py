import sqlite3
import os
connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()

def create_table(statement):
    cursor.execute(statement)
    connection.commit()

def insert_values(statement,data):
    cursor.execute(statement,data)
    connection.commit()

def find_movies(cmd,path):
    os.chdir(path)
    for (dirname, dirs, files) in os.walk('.'):
        for filename in files:
            if filename.endswith('.mp4') or filename.endswith('.mkv') or filename.endswith('avi') or filename.endswith('mp3'):
                dirname_new = dirname[2:]
                thefile = os.path.join(path,dirname_new,filename)
                filename_new = filename.replace('.',' ')[:(len(filename)-4)].lower()
                print thefile + " " + filename_new
                insert_values(cmd,(thefile,filename_new))
            

val = """CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
name TEXT NOT NULL,
sex TEXT NOT NULL)"""

val1 = """CREATE TABLE response(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
question TEXT NOT NULL,
answer TEXT NOT NULL,
added_by TEXT)"""

val2 = """CREATE TABLE movies(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
url TEXT NOT NULL,
name TEXT NOT NULL)"""

path = [r"M:\bolly",r"M:\new",r"M:\movies",r"E:\movies",r"D:\movies",r"M:\Animated"]
cmd = "INSERT INTO movies(url,name) VALUES (?,?)"

#create_table(val2)

for value in path:
    find_movies(cmd,value)

