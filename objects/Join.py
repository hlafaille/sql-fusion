"""
Simple declaration for which join mode the user requests
"""


class JoinModes:
    LEFT = 0
    RIGHT = 1


"""
This class is used for performing a typical SQL JOIN command. 
Takes two columns, a pretty name as required input, will be used on SQL generation.
A join mode can also be specified as an optional argument, which will determine whether 
the join type is LEFT or RIGHT.

Example:
SELECT sales_orders.*, customers.company_name FROM sales_orders 
LEFT JOIN customers ON sales_orders.customer=customers.id
"""


class Join:
    def __init__(self, column_1: str, column_2: str, pretty_name: str, join_mode=0):
        self.column_1 = column_1
        self.column_2 = column_2
        self.pretty_name = pretty_name
        self.join_mode = join_mode
