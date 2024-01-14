import sqlite3

import pygame

import pygame_menu
from pygame_menu import themes

from menu import startScreen
from FINAL import finalScreen


def addState(state):  # почему то не работает :(
    connection = sqlite3.connect('starry_rain1.sqlite')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO LastState (State) VALUES (?)", state)
    connection.commit()
    connection.close()


def checkState():
    connection = sqlite3.connect('starry_rain1.sqlite')
    cursor = connection.cursor()
    currentState = cursor.execute("SELECT * FROM table ORDER BY id DESC LIMIT 1")
    print(currentState)
    connection.commit()
    connection.close()


addState('MENU')
startScreen()
checkState()
