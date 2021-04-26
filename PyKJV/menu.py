

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

