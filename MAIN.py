import sqlite3

import pygame

import pygame_menu
from pygame_menu import themes

from menu import startScreen
from FINAL import finalScreen


def addState(state):
    connection = sqlite3.connect('starry_rain1.sqlite')
    cursor = connection.cursor()
    prev_id = cursor.execute("""SELECT id FROM LastState ORDER BY id DESC limit 1""").fetchall()
    id1 = prev_id[0][0]
    cursor.execute("INSERT INTO LastState (id, State) VALUES (?, ?)", (id1 + 1, state))
    connection.commit()
    connection.close()


# addState('MENU')


def checkState():
    connection = sqlite3.connect('starry_rain1.sqlite')
    cursor = connection.cursor()
    currentState = cursor.execute("SELECT * FROM LastState ORDER BY id DESC LIMIT 1").fetchall()
    connection.commit()
    connection.close()
    return currentState[0][1]


startScreen()
print(checkState())
