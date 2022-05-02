"""
Key-Value pair for storing a datatype. Must be Python datatype. Only supports case-sensitive database names.

ex:
If the name of your column is 'status', this object name argument should be the same.
"""


class Column:
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype
