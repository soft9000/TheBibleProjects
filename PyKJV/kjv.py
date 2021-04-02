#!/usr/bin/env python3
"""
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
"""

import sqlite3
import argparse
from verse import Verse
from sierra_dao import SierraDAO

display = Verse()


def say_done():
    """ What we see whenever a menu is done. """
    print("(exit)")


def do_menu(name, prompt, options, level):
    """ The menu loop - nice for nesting 'till we're done. """
    choice = None
    while choice != options[-1][0]:
        print(f"*** {name} ***")
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
    """ Show a book:chapter:verse """
    cvn = input("Enter chap:book#:vers# = ").strip()
    zset = SierraDAO.ParseClassicVerse(cvn)
    if not zset == False:
        dao = SierraDAO.GetDAO()
        zverse = dao.get_sierra_num(zset["book"], zset["chapter"], zset["verse"])
        if zverse:
            display.show(display.get_verse(zverse))


def do_book_vnum():
    """ Show a 1's based sierra verse number """
    cvn = input("Verse #: ").strip()
    if cvn:
        dao = SierraDAO.GetDAO()
        zverse = dao.get_sierra(cvn)
        if zverse:
            display.show(display.wrap(zverse["text"]))


def do_lookups():
    """ Ways to lookup books & verses """
    options = [
        ("l", "List Books", do_list),
        ("c", "Classic book:chapter:verse", do_book_cv),
        ("s", "Sierra #", do_book_vnum),
        ("q", "Quit", say_done),
    ]
    do_menu("Find Verse", "Option = ", options, "?")


def do_list():
    for line in display.list_books():
        print(f" | {line} |")


def do_random():
    """ Display a random verse. """
    display.show(display.random())


def do_find(s_num):
    """ Find a verse using the unique verse / Sierra number """
    display.show(display.get_verse(s_num))


def do_find_cvn(cvn):
    """ Find a verse using the classic chapter:book:verse notation """
    ref = SierraDAO.ParseClassicVerse(cvn)
    if not ref:
        print(f"(Verse '{cvn}' not found.)")
        return
    dao = SierraDAO.GetDAO()
    s_num = dao.get_sierra_num(ref["book"], ref["chapter"], ref["verse"])
    display.show(display.get_verse(s_num))


def parse_cmd_line():
    """ Return True if a commnd-line option was run, else False """
    HelpInformation = "kjv.py: Search, bookmark & browse the Bible."
    parse = argparse.ArgumentParser(usage="", description=HelpInformation)
    Parser = parse.add_mutually_exclusive_group()
    Parser.add_argument(
        "-r", "--Random", action="store_true", help="Get a random Bible verse"
    )
    Parser.add_argument("-l", "--List", action="store_true", help="List Bible books")
    Parser.add_argument("-s", "--Sierra", action="store_true", help="Find verse by #")
    Parser.add_argument(
        "-v", "--Verse", action="store_true", help="Find verse by chapter:book:verse"
    )
    args = parse.parse_args()
    if args.Random == True:
        do_random()
        return True
    if args.List == True:
        do_list()
        return True
    if args.Sierra == True:
        do_find(123)  # TODO: Need to accept a number, then call something else wth it.
        return True
    if args.Verse == True:
        do_find_cvn(
            "gene:1:3"
        )  # TODO: Need to accept a CVN, then call something else wth it.
        return True
    return False


if not parse_cmd_line():
    options = [
        ("r", "Random Verse", do_random),
        ("b", "Book List", do_list),
        ("s", "Show Verse", do_lookups),
        ("q", "Quit Program", say_done),
    ]
    do_menu("Main Menu", "Option = ", options, "#")
print(".")
