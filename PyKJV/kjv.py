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
    """ The menu loop - nice for nesting 'till we're done. """
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
    while True:
        cvn = input("Enter chap:book#:vers# = ").strip()
        if SierraDAO.IsValidVerse(cvn):
            pass
        # TODO: Finish up!
        break
    print("Work in progress: Soon!")


def do_book_vnum():
    ''' Locate by a 1's based sierra verse number '''
    pass


def do_lookups():
    ''' The ways to lookup books & verses '''
    options = [("b", "List Books", do_list),
               ("c", "book:chapter:verse", do_book_cv),
               ("a", "absolute verse #", do_book_vnum),
               ("q", "Quit", say_done)]
    do_menu("Search Menu: Option = ", options, '?')


def do_list():
    for line in Verse().list_books():
        print(f' | {line} |')


def do_random():
    lines = Verse().random()
    for line in lines:
        print(line)


def parse_cmd_line():
    HelpInformation = "kjv.py: Search, bookmark & browse the Bible."
    parse = argparse.ArgumentParser(usage='', description=HelpInformation)
    Parser = parse.add_mutually_exclusive_group()
    Parser.add_argument("-r",
                        "--Random",
                        action="store_true",
                        help="Search for a random verse in the bible")
    Parser.add_argument("-l",
                        "--List",
                        action="store_true",
                        help="List the books included in this software")
    Parser.add_argument("-s",
                        "--Search",
                        action="store_true",
                        help="Search for a specific verse in the bible")
    args = parse.parse_args()
    option = ""

    if args.Random == True:
        option = "r"
    elif args.List == True:
        option = "l"
    elif args.Search == True:
        option = "s"
    return option


option = parse_cmd_line()
if option:
    if option == "r":
        do_random()
    elif option == "l":
        do_list()
    elif option == "s":
        do_lookups()
else:
    options = [("r", "Random Verse", do_random), ("b", "List Books", do_list),
               ("s", "Search", do_lookups), ("q", "Quit", say_done)]
    do_menu("Main Menu: Option = ", options, 15)
print(".")
