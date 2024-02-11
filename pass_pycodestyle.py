#!/usr/bin/python3
"""Define a class that inherits from list"""


class MyList(list):
    """
    Define a class that inherits from list
    Args:
        list (lsit): list of string
    """

    def print_sorted(self):
        """Prints sorted ascending list"""
        new_list = self[:]
        new_list.sort()
        print(new_list)
