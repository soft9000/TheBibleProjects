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

from Pagination import Page

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


def do_menu_display(name, prompt, options):
    choice = None
    while choice != options[-1][0]:
        print(f"*** {name} ***")
        for o in options:
            print(o[0], o[1])
        choice = input(prompt)

        return choice.upper()


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
    options = [
        ("n", "Next Verse"),
        ("p", "Previous Verse"),
        ("q", "Quit Classic Verse"),
    ]
    option = None
    Statement = Statement.split()
    while True:
        option = do_menu_display("Page Menu", "Option = ", options)

        # next page
        if option.upper() == "n":
            Statement[2] = int(Statement[2]) + 10
            zpage = Page(Statement)
            verse = zpage.page_up()

            # if you did not receive a verse....
            if len(verse) == 0:

                # construct a count statement to retrieve the total number of verses
                Total_Pages = zpage.count_chapter_verses(
                    Statement[0], Statement[1])
                Total_Chapters = zpage.count_books_chapters(Statement[0])

                # if your trying to get a chapter that is not within the book. then switch to the next book
                if int(Statement[1]) >= Total_Chapters:

                    BookTitle = SierraDAO.GetBookId(Statement[0]) + 1
                    BookTitle = zpage.retrieve_title(BookTitle)

                    Statement[0] = BookTitle
                    Statement[1] = 1
                    Statement[2] = 0

                    verse = Page(Statement)
                    verse = verse.page_up()
                # if the verse we are currently at is equal to or greater than the page count "number of verses in our book" then turn the chapter
                elif Statement[2] >= Total_Pages:

                    Statement[1] = int(Statement[1]) + 1
                    Statement[2] = 0
                    verse = Page(Statement)
                    verse = verse.page_up()

            for n in verse:
                zformat = display.wrap(n[0])
                display.show(zformat)

        # page down
        elif option.upper() == "p":
            Statement[2] = int(Statement[2]) - 10
            zpage = Page(Statement)
            verse = zpage.page_down()

            # if you did not receive a verse....
            if len(verse) == 0:
                # construct a count statement to retrieve the total number of verses
                Total_Pages = zpage.count_chapter_verses(
                    Statement[0], Statement[1])
                Total_Chapters = zpage.count_books_chapters(Statement[0])

                # if your trying to get a chapter that is not within the book. then switch to the next book
                if int(Statement[1]) >= Total_Chapters:
                    BookTitle = SierraDAO.GetBookId(Statement[0]) - 1
                    BookTitle = zpage.retrieve_title(BookTitle)

                    Statement[0] = BookTitle
                    Statement[1] = 1
                    Statement[2] = 0

                    verse = Page(Statement)
                    verse = verse.down()
                # if the verse we are currently at is equal to or greater than the page count "number of verses in our book" then turn the chapter
                elif Statement[2] >= Total_Pages:
                    Statement[1] = int(Statement[1]) - 1
                    Statement[2] = 0
                    verse = Page(Statement)
                    verse = verse.page_up()

        elif option.upper() == "q":
            break


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

            do_find_cvn(

                args.Verse
            )
            turn_page(args.Verse)
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
