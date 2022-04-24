class JoinModes:
    LEFT_JOIN = 0
    RIGHT_JOIN = 1


"""
A simple carrier object, holds a left and right column for use on JOIN statements
"""


class JoinCondition:
    def __init__(self, left_column, right_column):
        self.left_column = left_column
        self.right_column = right_column


"""
This class is intended for use where you would use a JOIN statement in SQL
"""


class JoinColumn:
    def __init__(self, database_name, mode, join_condition: JoinCondition):
        self.database_name = database_name
        self.mode = mode
        self.join_condition = join_condition
