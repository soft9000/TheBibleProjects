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

import argparse
from sierra_dao import SierraDAO


def dum():
    print('(done)')


def do_func(prompt, options, level):
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
    pass


def do_book_vnum():
    pass


def do_search():
    options = [
    ("b", "List Books", do_list),
    ("c", "book:chapter:verse", do_book_cv),
    ("a", "absolute verse #", do_book_vnum),
    ("q", "Quit", dum)
    ]
    do_func("Search Menu: ", options, '?')


def do_list():
    pass


def do_random():
    pass


options = [
    ("r", "Random Verse", do_random),
    ("b", "List Books", do_list),
    ("s", "Search", do_search),
    ("q", "Quit", dum)
]

do_func("Main Menu: ", options, '#')
print(".")
