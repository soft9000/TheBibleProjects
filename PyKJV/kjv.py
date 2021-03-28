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


'''def do_menu(prompt, options, level):
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
'''
def do_menu(prompt, options, level):
    choice = True
    while choice == True:
        print(level * 15)
        if options.lower() == "r" or options.lower() == "-r":
            do_random()
            options =input('r Random Verse\nb List Books\ns Search\nq Quit\nMain Menu:')
        elif options.lower() == "l" or options.lower() == "-l":
            do_list()
            options =input('r Random Verse\nb List Books\ns Search\nq Quit\nMain Menu:')
        elif options.lower() == "s" or options.lower() == "-s":
            do_lookups()
            options =input('r Random Verse\nb List Books\ns Search\nq Quit\nMain Menu:')
        elif options.lower() == "q" or options.lower() == "-q":
            options =say_done()
            choice = False
        else:
            options =input('r Random Verse\nb List Books\ns Search\nq Quit\nMain Menu:')
            continue
    

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
#Evan Nagy
def Cmd_Line_Args():
    #Evan Nagy
    HelpInformation = "This Bible Software provides allows you to search the bible for specific verses"
    parse = argparse.ArgumentParser(usage='',description=HelpInformation)
    Parser = parse.add_mutually_exclusive_group()
    Parser.add_argument("-r","--Random",action="store_true",help="Search for a random verse in the bible")
    Parser.add_argument("-l","--List",action="store_true",help="List the books included in this software")
    Parser.add_argument("-s","--Search",action="store_true",help="Search for a specific verse in the bible")
    Parser.add_argument("-q","--Quit",action="store_true",help="Quits the program all together")
    args = parse.parse_args()

    option = ""

    if args.Random == True:
        option = "r"
    elif args.List == True:
        option = "l"
    elif args.Search == True:
        option = "s"
    elif args.Quit == True:
        option = "q"
    return option

'''options = [
    ("r", "Random Verse", do_random),
    ("b", "List Books", do_list),
    ("s", "Search", do_lookups),
    ("q", "Quit", say_done)
]'''

option = Cmd_Line_Args()

do_menu("Main Menu: ", option, '#')
print(".")
