"""
A basic data storage object for holding a reference to a column name
"""
class Column:
    def __init__(self, column: str):
        self.column_name = column


"""
This is a class that handles storing columns
"""
class ColumnHolder:
    def __init__(self):
        self.columns = []

    def add_column(self, column: Column):
        pass
