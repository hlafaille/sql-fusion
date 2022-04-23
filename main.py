from factories.DataclassFactory import DataclassFactory
from objects.SQLColumn import Column
from objects.SchemaAlias import SchemaAlias
from objects.SchemaMap import SchemaMap, RootSchemaMap

if __name__ == "__main__":
    schema = RootSchemaMap(columns=[
        SchemaAlias(database_name="incremental", pretty_name="id", datatype=int),
    ],
        root_name="CustomerReturn")

    dataclass_factory = DataclassFactory(schema)
