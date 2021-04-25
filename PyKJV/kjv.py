#!/usr/bin/env python3
"""
File: kjv.py
Problem Domain: Console Application
Status: WORK IN PROGRESS
Revision: 0.02

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
import mark_dao

from Pagination import Page, PageOps

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
    if zset == False:
        display.show(None)
    else:
        dao = SierraDAO.GetDAO()
        zverse = dao.get_sierra_num(
            zset["book"], zset["chapter"], zset["verse"])
        if zverse:
            display.show(display.get_verse(zverse))

    turn_page(cvn)


def do_book_vnum():
    """ Show a 1's based sierra verse number """
    cvn = input("Verse #: ").strip()
    if cvn:
        dao = SierraDAO.GetDAO()
        zverse = dao.get_sierra(cvn)
        if zverse:
            display.show(display.wrap(zverse["text"]))

def do_read_from():
    """Print ten verses"""
    cvn = input("From Verse #: ").strip()
    if cvn:
        dao = SierraDAO.GetDAO()
        loop = True
        while loop:
            zverses = dao.get_from_place(cvn)
            if zverses:
                for zverse in zverses:
                    display.show(display.wrap(format_num_with_text(zverse[0],zverse[1])))

            print("~~~~~~~~~~")
            cntn = input("Page (u)p, (d)own, (m)ark, (r)eview marks, or (q)uit: ")
            if cntn == "u":
                cvn = int(cvn) + 10
            if cntn == "d":
                cvn = int(cvn) - 10
            if cntn == "q":
                loop = False
            if cntn == "m":
                markerone = int(input("Which verses do you want start at? "))
                markertwo = int(input("Stop at what verse?" ))
                together = mark_dao.BookMark(markerone,markertwo)
                mark_dao.BookMarks.Sync(together)
                print("Marked")
            if cntn == "r":
                do_read_bkmrk()
                break
            print("~~~~~~~~~~")

def format_num_with_text(num, txt):
    result = str(num) + ': ' + txt
    return result

def do_read_bkmrk():
    
    loop = True
    while loop:
        oblist = mark_dao.BookMarks.Read()
        for x in oblist:
            print(x.__dict__)
        cmd = input("(d)elete, (u)pdate, (r)ead from or (q)uit: ")
        if cmd == "d":
            rem = int(input("Delete ID: "))
            todelete = mark_dao.BookMark(0,0,rem)
            mark_dao.BookMarks.Delete(todelete)
        if cmd == "u":
            first = int(input("New Start: "))
            middle = int(input("New End: "))
            last = int(input("Original ID: "))
            concatinate = mark_dao.BookMark(first,middle,last)
            mark_dao.BookMarks.Sync(concatinate)
        if cmd == "q":
            loop = False
        if cmd == "r":
            do_read_from()
            break


def do_lookups():
    """ Ways to lookup books & verses """
    options = [
        ("l", "List Books", do_list),
        ("c", "Classic book:chapter:verse", do_book_cv),
        ("s", "Sierra #", do_book_vnum),
        ("r", "Read From", do_read_from),
        ("b", "Manage Bookmarks", do_read_bkmrk),
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
    #ref = SierraDAO.ParseClassicVerse(cvn)
    for ref in cvn:
        if not ref:
            print(f"(Verse '{cvn}' not found.)")
            return
    dao = SierraDAO.GetDAO()
    s_num = dao.get_sierra_num(SierraDAO.GetBookId(
        cvn[0]), int(cvn[1]), int(cvn[2]))
    display.show(display.get_verse(s_num))


def turn_page(Statement):
    Statement = Statement.split()
    ops = PageOps(Statement)
    options = [
        ("n", "Next Verse", ops.do_next_page),
        ("p", "Previous Verse", ops.do_last_page),
        ("q", "Quit Classic Verse", say_done),
    ]
    do_menu("Verse Ref", "Option = ", options, "%")


def parse_cmd_line():
    """ Return True if a commnd-line option was run, else False """
    help_information = "kjv.py: Search, bookmark & browse the Bible."
    parse = argparse.ArgumentParser(usage="", description=help_information)

    parse.add_argument(
        "-s", "--Sierra", type=int, metavar="", help="Find verse by #")
    # Returns a list
    parse.add_argument(
        "-v", "--Verse", metavar="", nargs="*", help="Find verse by chapter:book:verse"
    )
    Parser = parse.add_mutually_exclusive_group()
    Parser.add_argument(
        "-r", "--Random", action="store_true", help="Get a random Bible verse"
    )
    Parser.add_argument("-l", "--List", action="store_true",
                        help="List Bible books")

    args = parse.parse_args()
    try:
        if args.Random == True:
            do_random()
            return True
        if args.List == True:
            do_list()
            return True
        if args.Sierra != None:
            do_find(args.Sierra)
            return True
        if len(args.Verse) >= 0:
            do_find_cvn(args.Verse)
            turn_page(args.Verse) # TODO: Please check this logic
            return True
        return False
    except:
        return False


if __name__ == '__main__':
    if not parse_cmd_line():
        options = [
            ("r", "Random Verse", do_random),
            ("b", "Book List", do_list),
            ("s", "Show Verse", do_lookups),
            ("q", "Quit Program", say_done),
        ]
        do_menu("Main Menu", "Option = ", options, "#")
    print(".")
