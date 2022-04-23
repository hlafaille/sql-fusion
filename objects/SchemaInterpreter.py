"""
This object iterates over a schema map and returns a JSON serializable dictionary
"""
from objects import SchemaMap


class SchemaInterpreter:
    def __init__(self, schema_map: SchemaMap.SchemaMap):
