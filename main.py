from objects.SQLColumn import Column
from objects.SchemaAlias import SchemaAlias
from objects.SchemaInterpreter import SchemaInterpreter
from objects.SchemaMap import SchemaMap

if __name__ == "__main__":
    schema = SchemaMap(
        [Column("isn", int),
         SchemaMap(columns=[
             SchemaAlias("customer_name", "name", str),
             SchemaAlias("customer_address_line1", "line1", str),
             SchemaAlias("customer_address_line2", "line2", str),
             SchemaAlias("customer_address_zip", "zip", int)],
             group_name="customer")]
    )

    interpreter = SchemaInterpreter(schema)

    for x in interpreter.master_json:
        print(x)
