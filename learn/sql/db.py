import sqlite3
import time
from datetime import date, datetime
from collections import namedtuple

GoalRecord = namedtuple("GoalsStruct", 'GoalID, GoalName, StartTime, Days, Info')

def drop_and_create(name):
    connection = sqlite3.connect(name)
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Goals;")
    cursor.execute('''  CREATE TABLE Goals (
                            GoalID      INTEGER         PRIMARY KEY AUTOINCREMENT,
                            GoalName    CHAR(255)       NOT NULL,
                            StartTime   DATE            NOT NULL,
                            Days        INTEGER         NOT NULL,
                            Info        VARCHAR(1024));''')
    connection.commit()
    return connection

def get_date():
    return date.fromtimestamp(time.time())

def add_goal(connection, GoalName, StartTime):
    cursor = connection.cursor()
    cursor.execute('''  INSERT INTO Goals (GoalName, StartTime, Days)
                        VALUES ("{}", "{}", 0)'''.format(GoalName, StartTime))
    connection.commit()
    return cursor.lastrowid

def get_goal(connection, GoalName):
    cursor = connection.cursor()
    cursor.execute('''  SELECT GoalID, GoalName, StartTime, Days FROM Goals
                        WHERE GoalName="{}"'''.format(GoalName))
    result = cursor.fetchone()
    return result

def load_goals(connection):
    cursor = connection.cursor()
    cursor.execute('''  SELECT GoalID, GoalName, StartTime, Days, Info FROM Goals''')
    goals = []
    for goal in map(GoalRecord._make, cursor.fetchall()):
        goals.append(goal)
    return goals

connection = drop_and_create('empty.sqlite')
connection = sqlite3.connect('empty.sqlite')
print(add_goal(connection, "Example1", get_date()))
print(add_goal(connection, "Example2", get_date()))
goals = load_goals(connection)
_date1 = datetime.strptime(goals[0].StartTime, "%Y-%m-%d")
_date2 = datetime.strptime(goals[1].StartTime, "%Y-%m-%d")
print((_date1 - _date2).days)
connection.close()