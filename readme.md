# daily

*Simple organization of things you want to do every n days.*

The main idea behind `daily` is that you might want to do something
every few days, but you might forget to do it, or life may be
easier with help organizing your system.
For example, you could use `daily` to cycle through a couple different
side projects, focusing on one each day. As other examples, you could set up
reminders to keep in touch with friends by saying hello every once in
a while, or use reminders to water your plants when you need to.

## Installation

    git clone https://github.com/tylerneylon/daily.git
    sudo ln -s $(cd daily; pwd)/daily.py /usr/local/bin/daily

## Help string

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

