#!/usr/bin/env python3
'''
File: kjv.py
Problem Domain: Console Application
Status: WORK IN PROGRESS
Revision: -1

MISSION
=======
Create a simple way to read & collect your favorite passages
using every operating system where Python is available.

NEXUS
----- 
https://github.com/soft9000/TheBibleProjects
'''

import sqlite3
import argparse
from verse import Verse
from sierra_dao import SierraDAO


def say_done():
    ''' What we see whenever we're done. '''
    print('(done)')


def do_menu(prompt, options, level):
    ''' The menu loop - nice for nesting 'till we're done. '''
    choice = None
    while choice != options[-1][0]:
        print(level * 15)
        for o in options:
            print(o[0], o[1])
        choice = input(prompt)
        if not choice:
            continue
        choice = choice[0].lower()
        print(f">> {choice}")
        for o in options:
            if o[0] == choice:
                o[2]()
                break


def do_book_cv():
    ''' Locate book:chapter:verse '''
    pass


def do_book_vnum():
    ''' Locate by a 1's based sierra verse number '''
    pass


def do_lookups():
    ''' The ways to lookup books & verses '''
    options = [
    ("b", "List Books", do_list),
    ("c", "book:chapter:verse", do_book_cv),
    ("a", "absolute verse #", do_book_vnum),
    ("q", "Quit", say_done)
    ]
    do_menu("Search Menu: ", options, '?')


def do_list():
    for line in Verse().list_books():
        print(f' | {line} |')


def do_random():
    lines = Verse().random()
    for line in lines:
        print(line)


options = [
    ("r", "Random Verse", do_random),
    ("b", "List Books", do_list),
    ("s", "Search", do_lookups),
    ("q", "Quit", say_done)
]

do_menu("Main Menu: ", options, '#')
print(".")
