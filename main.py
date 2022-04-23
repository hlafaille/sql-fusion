from cli.CommandInterpreter import CommandInterpreter
from factories.DataclassFactory import DataclassFactory
from objects.SQLColumn import Column
from objects.SchemaAlias import SchemaAlias
from objects.SchemaMap import SchemaMap, RootSchemaMap

if __name__ == "__main__":
    command_interpreter = CommandInterpreter()

    #dataclass = DataclassFactory(schema)
