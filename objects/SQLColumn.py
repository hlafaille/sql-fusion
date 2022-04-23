"""
Key-Value pair for storing a datatype. Must be Pythonic
"""


class Column:
    def __init__(self, name, python_datatype):
        self.name = name
        self.python_datatype = python_datatype