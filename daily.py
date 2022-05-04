#!/usr/bin/env python3
""" daily.py

    Usage:

        daily     # Print out today's item.

        daily -l  # List all of this year's items.

    (Assuming you've got a `daily` link to this script in your path.)

    Uses the file `~/.daily.json` in order to suggest today's reminder.  The
    stucture of the file is a list of n items, each of which is either a string
    or a list.

    This examines item (day_of_year) mod (n). If that item is a string, then
    that items is suggested. If that item is a list, then this script suggests
    the (k mod len(list))th item in the list, where k is the previous number of
    times this list has been hit within this year.

    In other words, if your main list has length n, then you are suggested the
    items in it once every n days, in a cycle. If you choose to use sublists,
    then that sublist is hit once every n days, and the items in that sublist
    are similarly cycled throughout the year.
"""
# TODO: Update the help string and readme to explain
#       named work tracks and independent reminders.

# ======================================================================
# Imports

import json
import sys

from datetime import date, timedelta
from pathlib import Path


# ======================================================================
# Constants

FILENAME = '.daily.json'


# ======================================================================
# Functions

def get_daily_filepath():
    """ If a path can be found to an existing daily.json file, this returns a
        Path object pointing to it. It first looks in ~, and then in the
        directory of this script itself. Otherwise, this returns None.
    """
    path = Path.home() / FILENAME
    if path.exists():
        return path
    path = Path(__file__).resolve().parent / FILENAME
    return path if path.exists() else None

def load_daily_items():
    filepath = get_daily_filepath()
    if filepath is None:
        print(__doc__)
        print('\nError:\n')
        print(f"I couldn't locate a {FILENAME} file.")
        print('You can place one in ~ or in the directory of this script.\n')
        sys.exit(1)
    with open(str(filepath)) as f:
        return json.load(f)

def print_day_and_item(daily_items, day, do_show_prefix=True):
    # The format is:
    # [Today] . Mon Apr 18 . i % n . item
    prefix = ' Today' if day == date.today() else '      '
    if not do_show_prefix:
        prefix = ''
    date_str = day.strftime('%a %b %d')
    index, item = get_item_for_day(daily_items, day)
    print_items = [prefix, date_str, f'{index:03}', item]
    if not do_show_prefix:
        del print_items[0]
    print(' . '.join(print_items))

def list_whole_year(daily_items):

    today = date.today()
    year  = today.year
    day   = today.replace(month=1, day=1)

    while day.year == year:
        print_day_and_item(daily_items, day)
        day += timedelta(days=1)

def get_item_from_list(index, items, name=None):
    """ Returns today's item (using `index` to understand what today is) from
        the list `items`, which may be a list of strings or of lists of strings.
        If `name` is provided, then the return value is f'{name}:[{item}]'.
    """
    i = index % len(items)
    item = items[i]
    if type(item) is not str:
        # See how many previous times we've hit this list so far this year.
        # As this resets every year this method currently favors earlier list
        # elements over later elements.
        nth_time = index // len(items)
        item = item[nth_time % len(item)]
    return item if name is None else f'{name}:[{item}]'

def get_item_for_day(daily_items, day):
    """ Returns index, item for `day`. """

    jan1 = day.replace(month=1, day=1)
    index = (day - jan1).days

    if type(daily_items) is list:
        return index, get_item_from_list(index, daily_items)

    # Otherwise, we're expecting to have a dictionary.
    assert type(daily_items) is dict

    reminders = []
    for key, value in daily_items.items():
        if type(value) is list:
            # Given a list, the key is the name of a track of work, and the
            # reminder for today is what to do within that track today.
            reminders.append(get_item_from_list(index, value, name=key))
        else:
            # Given an integer, the key is the reminder string itself, and
            # the integer is how many days to wait between reminders.
            assert type(value) is int
            if index % value == 0:
                reminders.append(key)

    return index, ', '.join(reminders)


# ======================================================================
# Main

def main():

    daily_items = load_daily_items()

    if len(sys.argv) == 2 and sys.argv[1] == '-l':
        list_whole_year(daily_items)
        sys.exit(0)

    if len(sys.argv) == 1:
        print_day_and_item(daily_items, date.today(), do_show_prefix=False)
        sys.exit(0)

    # If we get here, we got weird command-line parameters. Barf out help.
    print(__doc__)
    print('\nUnrecognized command-line parameter.\n')
    sys.exit(2)

if __name__ == '__main__':
    main()
